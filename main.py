# main.py
import sys
from parser_2 import parse # You need to provide this function in your parser module
from virtual_machine2 import execute # You need to provide this function in your virtual_machine module

def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            parse(file) # This would parse the file and generate the .obj file
            execute(file + '.obj') # This would execute the .obj file
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
