from utils import *


if __name__ == '__main__':
    getFileLoc()

    for location in file_path:
        parse(location)