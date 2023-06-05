from collections import deque

# Define the semantic cube
semantic_cube = {
    '+': {
        'int': {
            'int': 'int',
            'float': 'float'
        },
        'float': {
            'int': 'float',
            'float': 'float'
        }
    },
    '-': {
        'int': {
            'int': 'int',
            'float': 'float'
        },
        'float': {
            'int': 'float',
            'float': 'float'
        }
    },
    '*': {
        'int': {
            'int': 'int',
            'float': 'float'
        },
        'float': {
            'int': 'float',
            'float': 'float'
        }
    },
    '/': {
        'int': {
            'int': 'int',
            'float': 'float'
        },
        'float': {
            'int': 'float',
            'float': 'float'
        }
    },
    '=': {
        'int': {
            'int': 'int',
            'float': 'int',
            'bool': 'bool'
        },
        'float': {
            'float': 'float',
            'int': 'float'
        },
        'bool': {
            'bool': 'bool'
        },
        'string': {
            'string': 'string'
        }
    },
    '==': {
        'int': {
            'int': 'bool'
        },
        'float': {
            'float': 'bool',
            'int': 'bool'
        },
        'bool': {
            'bool': 'bool'
        },
        'string': {
            'string': 'bool'
        }
    },
    '!=': {
        'int': {
            'int': 'bool'
        },
        'float': {
            'float': 'bool',
            'int': 'bool'
        },
        'bool': {
            'bool': 'bool'
        },
        'string': {
            'string': 'bool'
        }
    },
    '<': {
        'int': {
            'int': 'bool',
            'float': 'bool'
        },
        'float': {
            'float': 'bool',
            'int': 'bool'
        }
    },
    '>': {
        'int': {
            'int': 'bool',
            'float': 'bool'
        },
        'float': {
            'float': 'bool',
            'int': 'bool'
        }
    },
    '<=': {
        'int': {
            'int': 'bool',
            'float': 'bool'
        },
        'float': {
            'float': 'bool',
            'int': 'bool'
        }
    },
    '>=': {
        'int': {
            'int': 'bool',
            'float': 'bool'
        },
        'float': {
            'float': 'bool',
            'int': 'bool'
        }
    },
    '&&': {
        'bool': {
            'bool': 'bool'
        }
    },
    '||': {
        'bool': {
            'bool': 'bool'
        }
    }
}

current_function = None

# Define the symbol table and the current scope
symbol_table = {}
current_scope = []

# Define the data types
data_types = ['int', 'float', 'bool', 'string']
temp_variable_counter = 0

# Define the quadruple structure
quadruples = []
operators_stack = []
operands_stack = []
types_stack = []

# Define the assignment stack
assignment_stack = []

# Definir la pila de saltos
jump_stack = []

# Constants Table
const_table = {}

# Functions Directory
dir_func = {}

# New dictionary for temp variables
temp_variables = {}
scopes_stack = []

# Define the memory spaces for variables
global_memory = {
    'int': 1000,
    'float': 2000,
    'bool': 3000,
    'string': 4000,
    'temp': 5000,
    'const': 6000
}

local_memory = {
    'int': 7000,
    'float': 8000,
    'bool': 9000,
    'string': 10000,
    'temp': 11000
}

temp_memory = {
    'int': 12000,
    'float': 13000,
    'bool': 14000,
    'string': 15000
}


# Function to create a new scope
def create_scope(scope_name):
    global current_scope
    global dir_func
    if scope_name not in dir_func:
        dir_func[scope_name] = {'local_variables': {}, 'param_list': [], 'start_quad': len(quadruples), 'num_params': 0}
    current_scope.append(scope_name)


# Function to end the current scope
def end_scope():
    global current_scope
    current_scope.pop()

# Function to declare a variable in the symbol table
def declare_variable(id, type):
    global dir_func
    global current_scope
    global local_memory
    global global_memory
    print(current_scope)
    print(id, type)
    if current_scope:
        if current_scope[-1] == 'global':
            # In the global scope, so allocate a global memory address
            memory_address = global_memory[type]
            global_memory[type] += 1
        else:
            # In a local scope, so allocate a local memory address
            memory_address = local_memory[type]
            local_memory[type] += 1
    else:
        raise Exception("No current scope to declare variable in.")

    variable_info = {'type': type, 'memory_address': memory_address}
    print(variable_info)
    # Adding variable to the local variables table of the current scope
    if 'local_variables' not in dir_func[current_scope[-1]]:
        dir_func[current_scope[-1]]['local_variables'] = {}

    dir_func[current_scope[-1]]['local_variables'][id] = variable_info

# Function to declare a constant in the ConstTable
def declare_constant(value, type):
    global const_table
    global global_memory

    if value not in const_table:
        memory_address = global_memory['const']
        global_memory['const'] += 1
        const_table[value] = {'type': type, 'memory_address': memory_address}

# Function to generate a new quadruple
def generate_quadruple(operator, left_operand, right_operand, result):
    global quadruples
    global temp_variables
    # Replacing variable names with memory addresses
    if isinstance(left_operand, str):
        if left_operand in temp_variables:
            left_address = temp_variables[left_operand]['memory_address']
        else:
            left_address = get_memory_address(left_operand)
    else:
        left_address = left_operand

    if isinstance(right_operand, str):
        if right_operand in temp_variables:
            right_address = temp_variables[right_operand]['memory_address']
        else:
            right_address = get_memory_address(right_operand)
    else:
        right_address = right_operand

    # If result is a temp variable, replace it with its memory address
    if isinstance(result, str) and result in temp_variables:
        result_address = temp_variables[result]['memory_address']
    else:  # If result is a normal variable or already-resolved memory address
        result_address = get_memory_address(
            result) if isinstance(result, str) else result
        
    print(operator, left_address, right_address, result_address)
    quadruples.append((operator, left_address, right_address, result_address))

# Function to get the type of a variable
def get_variable_type(variable_name):
    global dir_func
    global current_scope

    for scope in reversed(dir_func):
        if variable_name in dir_func[scope]['local_variables']:
            return dir_func[scope]['local_variables'][variable_name]['type']
    return None

# Function to get the memory address of a variable
def get_memory_address(variable_name):
    # Check in local variables
    for scope in reversed(dir_func):  # Start from the innermost scope
        if variable_name in dir_func[scope]['local_variables']:
            return dir_func[scope]['local_variables'][variable_name]['memory_address']

    # Check in global variables
    if variable_name in dir_func['global']:
        return dir_func['global'][variable_name]['memory_address']

    # Check in constants
    if variable_name in const_table:
        return const_table[variable_name]['memory_address']

    # Check in temp variables
    if variable_name in temp_variables:
        return temp_variables[variable_name]['memory_address']

    return None

def print_quadruples():
    global quadruples
    print("Quadruples:")
    for i, quad in enumerate(quadruples):
        print(f"{i}: {quad}")

# Function to add a variable to the symbol table
def add_variable_to_symbol_table(variable_name, variable_type, scope=None):
    global dir_func
    global current_scope
    if scope is None:
        scope = current_scope[-1]
    memory_address = get_next_available_memory_address(variable_type)
    dir_func[scope]['local_variables'][variable_name] = {
        'type': variable_type, 'memory_address': memory_address}

# Function to check if a variable has already been declared
def check_variable_declared(variable_name, scope=None):
    global dir_func
    global current_scope
    if scope is None:
        scope = current_scope[-1]
        print('checking', scope)
    # Check local variables
    if 'local_variables' in dir_func[scope] and variable_name in dir_func[scope]['local_variables']:
        return True

    # Check global variables
    if 'global' in dir_func and variable_name in dir_func['global']:
        return True

    return False


# Function to get the next available memory address
def get_next_available_memory_address(data_type, is_temp=False):
    global global_memory
    global local_memory
    global temp_memory
    memory_address = None
    if is_temp:
        if data_type in temp_memory:
            memory_address = temp_memory[data_type]
            temp_memory[data_type] += 1
    else:
        if data_type in global_memory:
            memory_address = global_memory[data_type]
            global_memory[data_type] += 1
        elif data_type in local_memory:
            memory_address = local_memory[data_type]
            local_memory[data_type] += 1
    return memory_address

# Function to add an operator to the operators stack
def add_operator_to_stack(operator):
    global operators_stack
    operators_stack.append(operator)

# Function to add an operand to the operands stack
def add_operand_to_stack(operand, data_type):
    global operands_stack
    global types_stack
    operands_stack.append(operand)
    types_stack.append(data_type)

# Function to create a temp variable and add it to the symbol table
def create_temp_variable(data_type):
    global temp_variable_counter
    global temp_variables

    temp_variable_name = f"t{temp_variable_counter}"
    temp_variable_counter += 1
    memory_address = get_next_available_memory_address(data_type, is_temp=True)

    # Store the variable name
    temp_variables[temp_variable_name] = {
        'type': data_type, 'memory_address': memory_address, 'name': temp_variable_name}

    # return variable name and memory address
    return temp_variable_name, memory_address


def start_if(condition_address):
    global quadruples
    global jump_stack
    # Create unfilled 'GotoF' quadruple
    quadruples.append(('GotoF', condition_address, None, None))
    jump_stack.append(len(quadruples) - 1)  # Save the 'GotoF' index


def else_part():
    global quadruples
    global jump_stack
    false_jump = jump_stack.pop()  # Get 'GotoF' index from the 'if' part
    # Create unfilled 'Goto' quadruple
    quadruples.append(('Goto', None, None, None))
    end_jump = len(quadruples) - 1  # Save the 'Goto' index
    # Fill 'GotoF' quadruple with the start of 'else' part
    quadruples[false_jump] = quadruples[false_jump][:3] + (len(quadruples),)
    jump_stack.append(end_jump)  # Save the 'Goto' index


def end_else():
    global quadruples
    global jump_stack
    if jump_stack:  # Check if there is a 'Goto' quadruple to fill
        end_jump = jump_stack.pop()  # Get 'Goto' index
        # Fill 'Goto' quadruple with the end of 'else' part
        quadruples[end_jump] = quadruples[end_jump][:3] + (len(quadruples),)


def end_if():
    global quadruples
    global jump_stack
    if jump_stack:  # Check if there is a 'Goto' quadruple to fill
        false_jump = jump_stack.pop()  # Get 'GotoF' index
        # Fill 'GotoF' quadruple with the current address
        quadruples[false_jump] = quadruples[false_jump][:3] + \
            (len(quadruples),)


def start_while():
    global quadruples
    global jump_stack
    # Create unfilled 'GotoF' quadruple
    print(len(quadruples))
    jump_stack.append(len(quadruples))  # Save the 'GotoF' index


def end_while():
    global quadruples
    global jump_stack
    # This points to start of while loop
    ret = jump_stack.pop()
    # Get the 'GotoF' quadruple index
    false_jump = jump_stack.pop()
    # Jump back to condition check
    quadruples.append(('Goto', None, None, false_jump))
    # Fill in jump destination in start_while
    quadruples[false_jump] = quadruples[false_jump][:3] + (len(quadruples) + 1,)

def handle_function_declaration(func_name, param_list, local_vars_list, return_type):
    global dir_func
    global quadruples
    global current_scope

    # Remove None entries from local_vars_list
    local_vars_list = [var for var in local_vars_list if var is not None]

    if func_name not in dir_func:
        raise Exception(f"Function {func_name} does not exist.")


    # Add the return_type to the current dir_func
    dir_func[func_name]['param_list'] = param_list
    for i, param in enumerate(param_list):
        # Create a new tuple with the modified content
        modified_param = param[:2] + (get_memory_address(param[2]),) + param[3:]
        # Replace the old tuple with the new one
        dir_func[func_name]['param_list'][i] = modified_param
    dir_func[func_name]['num_params'] = len(param_list)
    dir_func[func_name]['return_type'] = return_type

    # Clear the local scope
    current_scope.pop()


def handle_function_call(func_name, arg_list):
    global dir_func
    global quadruples
    global stack_operands

    # Check if the function exists
    if func_name not in dir_func:
        raise Exception(f"Function {func_name} not declared.")

    # Generate an ERA action for the function call
    quadruples.append(('ERA', func_name, None, None))

    # Verify and process arguments
    if len(arg_list) != dir_func[func_name]['num_params']:
        raise Exception(
            f"Function {func_name} called with incorrect number of arguments.")

    for i, arg in enumerate(arg_list):
        arg_type = get_expression_type(arg)
        param_type = dir_func[func_name]['param_list'][i][1]
        param_address = get_memory_address(arg)
        if arg_type != param_type:
            raise Exception(f"Type mismatch in argument {i+1} of function {func_name} call.")

        # Generate PARAMETER action
        quadruples.append(('PARAMETER', param_address, None, i))

    # Generate GOSUB action
    quadruples.append(
        ('GOSUB', func_name, None, dir_func[func_name]['start_quad']+1))

    if dir_func[func_name]['return_type'] is not 'void':
        return_var_name = dir_func[func_name]['return_var']
        return_var_address = get_memory_address(return_var_name)
        temp_var_name = create_temp_variable(dir_func[func_name]['return_type'])
        declare_variable(temp_var_name[0], dir_func[func_name]['return_type'])
        quadruples.append(('ASSIGN', return_var_address, None, temp_var_name[1]))
        operands_stack.append(temp_var_name[1])
        types_stack.append(dir_func[func_name]['return_type'])


def current_func_name():
    # assuming dir_func is your function directory
    return list(dir_func.keys())

def handle_function_return(return_expr, func_name):
    global dir_func
    global quadruples
    # Check the function has a return type
    if 'return_type' not in dir_func[func_name] or dir_func[func_name]['return_type'] is None:
        raise Exception(f"Function {func_name} does not have a return type.")

    # Check the type of the return expression matches the function's return type
    # Fetch the return variable details from the VarTable
    if return_expr not in dir_func[func_name]['local_variables']:
        raise Exception(f"Return variable {return_expr} not found in function {func_name}.")
    
    return_var = dir_func[func_name]['local_variables'][return_expr]
    return_expr_type = return_var['type']
    return_var_address = return_var['memory_address']
    
    if return_expr_type is None or return_expr_type != dir_func[func_name]['return_type']:
        raise Exception(
            f"Return type mismatch in function {func_name}. Expected {dir_func[func_name]['return_type']}, got {return_expr_type}.")

    # Generate an action to return the return expression to the calling function
    quadruples.append(('RETURN', None, None, return_var_address))


def get_expression_type(expression):
    global dir_func
    global current_scope

    if len(expression) == 1:
        token = expression[0]
        if isinstance(token, str):  # Variable
            return get_variable_type(token)
        elif isinstance(token, int):  # Integer literal
            return 'int'
        elif isinstance(token, float):  # Float literal
            return 'float'
        else:
            raise Exception(f"Unknown token type: {type(token)}")
    else:  # Complex expression
        # For simplicity, assume all variables in the expression are of the same type
        var_type = get_variable_type(expression[0])
        for token in expression[2::2]:  # Only check the variables
            if get_variable_type(token) != var_type:
                raise Exception(f"Type mismatch in expression: {expression}")
        return var_type  # Return the type of the variables
    
    
def declare_array(id, type, dimensions):

    dir_func[current_scope[-1]]['local_variables'][id] = {'type': type, 'isArray': True}


    dimensions_node = []
    DIM = 1
    R = 1


    for LiDIM, LSDIM in dimensions:
        R = (LSDIM - LiDIM + 1) * R
        dimensions_node.append({'LiDIM': LiDIM, 'LSDIM': LSDIM, 'DIM': DIM, 'mDIM': 0})
        DIM += 1


    DIM = 1
    OffSet = 0
    Size = R
    for node in dimensions_node:
        mDIM = R / (node['LSDIM'] - node['LiDIM'] + 1)
        node['mDIM'] = mDIM
        R = mDIM
        OffSet = OffSet + node['LiDIM'] * mDIM
        DIM += 1
    K = OffSet


    dimensions_node[-1]['K'] = -K


    dir_func[current_scope[-1]]['local_variables'][id]['virtual_address'] = global_memory[type]


    global_memory[type] += Size


    dir_func[current_scope[-1]]['local_variables'][id]['dimensions'] = dimensions_node
    print(dir_func)

# def array_access(id, index_expr):
#     if not isinstance(index_expr, int):
#         raise Exception("Array index must be an integer")

#     var_info = check_variable_declared(id)
#     if var_info is None:
#         raise Exception(f"Variable {id} is not declared")
#     if not var_info['isArray']:
#         raise Exception(f"Variable {id} is not an array")

#     dimensions = var_info['dimensions']
#     if index_expr < dimensions[0]['LiDIM'] or index_expr > dimensions[0]['LSDIM']:
#         raise Exception(f"Array {id} index out of range")

#     memory_address = var_info['memory_address'] + index_expr
#     return memory_address  # return the memory address of the array element

# def array_assign(id, index_expr, value):
#     memory_address = array_access(id, index_expr)

#     # assignment operation
#     memory[memory_address] = value
