from services.flags_parser import FlagsParser
from services.proyect_builder import ProyectBuilder
from file.dot_aku_writer import DotAkuWriter

def main():
    fg = FlagsParser().build()
    flags: dict[str, str] = fg.get_flags()
    proyect = (
        ProyectBuilder(proyect_name=flags["proyect_name"])
        .build_parent_folder(flags["output_folder_path"])
        .build_data_folder(flags["proyect_data_folder"])
        .build_bin_folder(flags["proyect_bin_folder"])
        .create_proyect()
        .copy_img_2_proyect(flags["input_img_path"])
        .copy_text_2_proyect(flags["input_text_path"])
    )
    
    DotAkuWriter(img_path=proyect.img_path,
                 text_path=proyect.text_path,
                 bin_file_path=proyect.bin_folder).write_file()


if __name__ == "__main__":
    main()