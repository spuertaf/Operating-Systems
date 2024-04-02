from services.flags_parser import FlagsParser
from file.dot_aku_reader import DotAkuReader

def main():
    fg = FlagsParser().build()
    flags: dict[str, str] = fg.get_flags()
    
    DotAkuReader(proyect_parent_folder=flags["proyect_parent_folder"]).parse()


if __name__ == "__main__":
    main()
