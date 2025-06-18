# tests.py

import unittest
from functions import get_file_content, get_files_info, write_file, run_python

def test():
    result = run_python.run_python_file("calculator", "main.py")
    print(result)
    
    result = run_python.run_python_file("calculator", "tests.py")
    print(result)
    
    result = run_python.run_python_file("calculator", "../main.py")
    print(result)
    
    result = run_python.run_python_file("calculator", "nonexistent.py")
    print(result)
        


if __name__ == "__main__":
    test()