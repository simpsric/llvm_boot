# tests.py

import unittest
from functions import get_files_content, get_files_info, write_file

def test():
    result = write_file.write_file(
        working_directory="calculator",
        file_path="lorem.txt",
        content="wait, this isn't lorem ipsum"
    )
    print(result)  # Expected: Successfully wrote to "subdir/test_file.txt"
    
    result = write_file.write_file(
        working_directory="calculator",
        file_path="pkg/morelorem.txt",
        content="lorem ipsum dolor sit amet"
    )
    print(result)  # Expected: Successfully wrote to "pkg/morelorem.txt"
    
    result = write_file.write_file(
        working_directory="calculator",
        file_path="/tmp/temp.txt",
        content="this should not work"
    )
    print(result)  # Expected: Error: Cannot write to "/tmp/temp.txt" as


if __name__ == "__main__":
    test()