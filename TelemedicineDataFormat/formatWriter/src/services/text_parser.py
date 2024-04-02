import os


class TextParser:
    """Parses text files.

    This class provides methods for parsing text files.

    Attributes:
        _text_path (str): The path to the text file.
    """

    def __init__(self, text_path: str):
        """Initializes a TextParser object.

        Args:
            text_path (str): The path to the text file.
        """
        self._text_path = os.path.abspath(text_path)
        
    def get_file_content(self) -> list[str]:
        """Gets the content of the text file.

        Returns:
            list[str]: The content of the text file as a list of strings.
        """
        with open(self._text_path, 'r') as text_file:
            content = text_file.read()
        text_file.close()
        file_content = content.split(";")
        file_content = map(lambda x: x.replace("\n", "").strip(), file_content)
        return list(file_content)
    
    
if __name__ == "__main__":
    print(TextParser("C:\\Users\\Admin\\Desktop\\Operating-Systems\\TelemedicineDataFormat\\formatWriter\\text\\sample1.txt").get_file_content())