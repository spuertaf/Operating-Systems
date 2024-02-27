from utils import multiply_mats, find_available_cores
from concurrent.futures import ProcessPoolExecutor
from functools import partial

import numpy as np


class ImageOperations:
    def _to_rads(self, angle: int):
        return angle*np.pi/180

    def calc_hypotenuse(self, x, y):
        return np.sqrt(x**2 + y**2)
    
    def calc_rotation_mat(self, angle: int) -> np.ndarray:
        rads_angle = self._to_rads(angle)
        rotation_mat = np.identity(3)
        rotation_mat[0,0] = np.cos(rads_angle)
        rotation_mat[0,1] = np.sin(rads_angle)
        rotation_mat[1,0] = -np.sin(rads_angle)
        rotation_mat[1,1] = np.cos(rads_angle)
        return rotation_mat
    
    def calc_transfer_mat(self, dx, dy):
        transfer_mat = np.identity(3)
        transfer_mat[0,2] = dx
        transfer_mat[1,2] = dy
        return transfer_mat
    
    def calc_new_img(self, result_mat, img, new_shape):
        img_xy_shape = img.shape[0:2]
        new_img = np.zeros(new_shape, dtype='u1')
        for x in range(img_xy_shape[0]):
            for y in range(img_xy_shape[1]):
                xyw = np.array([x,y,1])
                new_xyw = multiply_mats(result_mat, xyw)
                new_img[int(new_xyw[0]),int(new_xyw[1])] = img[x,y]
        return new_img
    
    def get_img_fragments(self, img: np.ndarray, num_fragments) -> list:
        img_xy_shape = img.shape[0:2]
        fragment_threshold = int(np.ceil(img_xy_shape[0]/num_fragments))
        return [(i*fragment_threshold, img[i*fragment_threshold:(i+1)*fragment_threshold]) 
                for i in range(num_fragments)]
    
    def get_fragment_rot_mat(self, angle, img_xy_shape, new_img_shape):
        height, width = img_xy_shape
            
        center_img_x, center_img_y = (-height//2, -width//2)
        center_canvas_x, center_canvas_y = (new_img_shape[0]//2, new_img_shape[1]//2)

        rotation_mat = self.calc_rotation_mat(angle)
        transfer_mat_center_img = self.calc_transfer_mat(center_img_x, center_img_y)
        transfer_mat_center_canvas = self.calc_transfer_mat(center_canvas_x, center_canvas_y)

        return multiply_mats(transfer_mat_center_canvas, rotation_mat, transfer_mat_center_img)
    

class Image:
    def __init__(self, img: np.ndarray):
        self._img = img
        self._img_ops = ImageOperations()

    def rotate(self, angle: int) -> np.ndarray:
        img_xy_shape = self._img.shape[0:2]
        height, width = img_xy_shape
        hypotenuse = self._img_ops.calc_hypotenuse(height, width)

        new_img_shape = (int(2*hypotenuse), int(2*hypotenuse), 3)

        center_img_x, center_img_y = (-height//2, -width//2)
        center_canvas_x, center_canvas_y = (new_img_shape[0]//2, new_img_shape[1]//2)

        rotation_mat = self._img_ops.calc_rotation_mat(angle)
        transfer_mat_center_img = self._img_ops.calc_transfer_mat(center_img_x, center_img_y)
        transfer_mat_center_canvas = self._img_ops.calc_transfer_mat(center_canvas_x, center_canvas_y)
        
        result_mat = multiply_mats(transfer_mat_center_canvas, rotation_mat, transfer_mat_center_img)
        rotated_img = self._img_ops.calc_new_img(result_mat, self._img.copy(), new_img_shape)
        return rotated_img
    
    def rotate_fragment(self,
                        idx_and_fragments, 
                        rotation_mat, 
                        img_rotation_mat, 
                        new_img_shape):
            fragment_x, fragment = idx_and_fragments

            fragment_translation_dir = np.array([fragment_x, 0, 1])
            fragment_translation_dir_rotated = multiply_mats(rotation_mat, fragment_translation_dir)

            translation_fragment_mat = self._img_ops.calc_transfer_mat(
                fragment_translation_dir_rotated[0],
                fragment_translation_dir_rotated[1]
            )
            fragment_result_mat = multiply_mats(translation_fragment_mat, img_rotation_mat)
            return self._img_ops.calc_new_img(fragment_result_mat, fragment.copy(), new_img_shape)


    def merge_fragments(self, fragments:list, new_img_shape):
        new_img = np.zeros(new_img_shape, dtype='u1')
        for fragment in fragments:
            new_img += fragment
        return np.array(new_img, dtype='u1')


    def rotate_paralelized(self, angle: int):
        idx_n_fragments:list = self._img_ops.get_img_fragments(self._img, find_available_cores())
        img_xy_shape = self._img.shape[0:2]
        img_hypotenuse = self._img_ops.calc_hypotenuse(*img_xy_shape)

        rotation_mat = self._img_ops.calc_rotation_mat(angle)
        new_img_shape = (int(2*img_hypotenuse), int(2*img_hypotenuse), 3)
        fragment_rot_mat = self._img_ops.get_fragment_rot_mat(angle, img_xy_shape, new_img_shape)
        
        partial_rotate_fragment = partial(self.rotate_fragment, rotation_mat=rotation_mat, img_rotation_mat=fragment_rot_mat, new_img_shape=new_img_shape)

        with ProcessPoolExecutor(max_workers=find_available_cores()) as executor:
            fragments:list = list(executor.map(partial_rotate_fragment, [fragment for fragment in idx_n_fragments]))

        return self.merge_fragments(fragments, new_img_shape)
