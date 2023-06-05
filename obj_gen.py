import json
from semantics import *

# Assuming dir_func, const_table, and quadruples are your data structures.
def generate_obj_file(filename, dir_func, const_table, quadruples):
    obj_file = {
        'DirFunc': dir_func,
        'ConstTable': const_table,
        'Quadruples': quadruples,
    }
    with open(filename, 'w') as file:
        json.dump(obj_file, file)
