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
assign_quad_stack = []

PilaO = []
PTipos = []
POper = []
PilaDim = []

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

    #print('Variable being added: ', variable_info, 'to: ', current_scope)
    dir_func[current_scope[-1]]['local_variables'][id] = variable_info

def declare_param_variable(id, type):
    global dir_func
    global current_scope
    global local_memory
    global global_memory

    if current_scope:
        if current_scope[-1] == 'global':
            # Parameters can't be declared in the global scope.
            raise Exception("Parameters cannot be declared in the global scope.")
        else:
            # In a local scope, so allocate a local memory address
            memory_address = local_memory[type]
            local_memory[type] += 1
    else:
        raise Exception("No current scope to declare variable in.")

    variable_info = {'type': type, 'memory_address': memory_address}

    dir_func[current_scope[-1]]['local_variables'][id] = variable_info
    dir_func[current_scope[-1]]['param_list'].append(variable_info)
    dir_func[current_scope[-1]]['num_params'] += 1

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

# Printing quadruples
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

# Function to start the conditional
def start_if(condition_address):
    global quadruples
    global jump_stack
    # Create unfilled 'GotoF' quadruple
    quadruples.append(('GotoF', condition_address, None, None))
    jump_stack.append(len(quadruples) - 1)  # Save the 'GotoF' index

# Function to process the else statement
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

# Function to end the else statement
def end_else():
    global quadruples
    global jump_stack
    if jump_stack:  # Check if there is a 'Goto' quadruple to fill
        end_jump = jump_stack.pop()  # Get 'Goto' index
        # Fill 'Goto' quadruple with the end of 'else' part
        quadruples[end_jump] = quadruples[end_jump][:3] + (len(quadruples),)

# Function to end the entire conditional
def end_if():
    global quadruples
    global jump_stack
    if jump_stack:  # Check if there is a 'Goto' quadruple to fill
        false_jump = jump_stack.pop()  # Get 'GotoF' index
        # Fill 'GotoF' quadruple with the current address
        quadruples[false_jump] = quadruples[false_jump][:3] + \
            (len(quadruples),)

# Function to start the while loop
def start_while():
    global quadruples
    global jump_stack
    # Create unfilled 'GotoF' quadruple
    jump_stack.append(len(quadruples))  # Save the 'GotoF' index

# Function to end the while loop
def end_while():
    global quadruples
    global jump_stack
    # This points to start of while loop
    ret = jump_stack.pop()
    # Get the 'GotoF' quadruple index
    false_jump = jump_stack.pop()
    # Jump back to condition check
    quadruples.append(('Goto', None, None, false_jump - 1))
    # Fill in jump destination in start_while
    quadruples[false_jump] = quadruples[false_jump][:3] + (len(quadruples),)

# Function to process the declaration of functions
def handle_function_declaration(func_name, param_list, local_vars_list, return_type):
    global dir_func
    global quadruples
    global current_scope

    # Remove None entries from local_vars_list
    local_vars_list = [var for var in local_vars_list if var is not None]

    if func_name not in dir_func:
        raise Exception(f"Function {func_name} does not exist.")
    dir_func[func_name]['return_type'] = return_type

    if dir_func[func_name]['return_type'] != 'void':
        return_var_name = dir_func[func_name]['return_var']
        return_var_address = get_memory_address(return_var_name)
        # Loop through all indices in the assign_quad_stack
        while assign_quad_stack:
            assign_quad_index = assign_quad_stack.pop()  # retrieve the index of ASSIGN quadruple
            result_address = quadruples[assign_quad_index][3] # = ('ASSIGN', None, None, 12001)
            quadruples[assign_quad_index] = ('ASSIGN', return_var_address, None, result_address)
    # Clear the local scope
    current_scope.pop()

# Function to process callings of functions    
def handle_function_call(func_name, arg_list):
    global dir_func
    global quadruples
    global stack_operands
    global assign_quad_stack

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
        param_type = dir_func[func_name]['param_list'][i]['type']
        if get_memory_address(arg) is not None:
            param_address = get_memory_address(arg)
        else:
            param_address = arg
        if arg_type != param_type:
            raise Exception(f"Type mismatch in argument {i+1} of function {func_name} call.")

        # Generate PARAMETER action
        quadruples.append(('PARAMETER', param_address, None, i))

    # Generate GOSUB action
    quadruples.append(
        ('GOSUB', func_name, None, dir_func[func_name]['start_quad']))

    if dir_func[func_name]['return_type'] != 'void':
        return_var_name = dir_func[func_name]['return_var']
        return_var_address = get_memory_address(return_var_name)
        if return_var_address is None:
            assign_quad_index = len(quadruples)  # get the current size of quadruples
            assign_quad_stack.append(assign_quad_index)  # keep track of ASSIGN quadruple
        temp_var_name = create_temp_variable(dir_func[func_name]['return_type'])
        declare_variable(temp_var_name[0], dir_func[func_name]['return_type'])
        quadruples.append(('ASSIGN', return_var_address, None, temp_var_name[1]))
        operands_stack.append(temp_var_name[1])
        types_stack.append(dir_func[func_name]['return_type'])

# Get the current function name
def current_func_name():
    return list(dir_func.keys())

# Handle returs of conditionals
def handle_function_return(return_expr, func_name):
    global dir_func
    global quadruples

    return_var = dir_func[func_name]['local_variables'][return_expr]
    return_var_address = return_var['memory_address']
    dir_func[func_name]['return_var'] = return_expr
    
    # Generate an action to return the return expression to the calling function
    quadruples.append(('RETURN', None, None, return_var_address))

# Function to get the type of any expr
def get_expression_type(expression):
    global dir_func
    global current_scope

    # If expression is a single number, handle it directly
    if isinstance(expression, (int, float)):
        return 'int' if isinstance(expression, int) else 'float'
    
    # If expression is a string (single variable), handle it directly
    if isinstance(expression, str):
        return get_variable_type(expression)

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
        var_type = get_variable_type(expression[0])
        for token in expression[2::2]:  # Only check the variables
            if get_variable_type(token) != var_type:
                raise Exception(f"Type mismatch in expression: {expression}")
        return var_type  # Return the type of the variables

# Arrays main function
def declare_array(id, type, size):
    global dir_func
    global current_scope
    global global_memory
    
    if isinstance(size, list):
        size = size[0]

    if not isinstance(size, int):
        raise TypeError("Size must be an integer")
    
    # Create the array variable in the current function scope
    dir_func[current_scope[-1]]['local_variables'][id] = {
        'type': type,
        'isArray': True,
        'virtual_address': global_memory[type],  # The base virtual address of the array
        'size': size
    }

    # Update the global memory index
    global_memory[type] += size

#Function to hanlde arrays
def handle_array_access(array_id, index_expression):
    array_info = dir_func[current_scope[-1]]['local_variables'][array_id]

    # Check if the index_expression is a temporary memory address
    if index_expression in temp_variables:
        indx_address = temp_variables[index_expression]['memory_address']
    else:
        # The address of index_expression is the evaluated result of index_expression
        indx_address = index_expression
    
    # Declare index_expression constant
    declare_constant(index_expression, 'int')
    indx_address = get_memory_address(index_expression)
    temp1, address1 = create_temp_variable('int')  # Assuming index_expression is of 'int' type
    quadruples.append(('=', indx_address, None, address1))

    # Generate quadruple for the verification
    lower_limit = array_info['dimensions'][0]['LiDIM']
    upper_limit = array_info['dimensions'][0]['LSDIM']
    declare_constant(lower_limit, 'int')
    lowLim_address = get_memory_address(lower_limit)
    declare_constant(upper_limit, 'int')
    uppLim_address = get_memory_address(upper_limit)
    quadruples.append(('VER', address1, lowLim_address, uppLim_address))

    # Generate quadruple for the K addition
    K = array_info['dimensions'][0]['K']
    declare_constant(K, 'int')
    K_address = get_memory_address(K)
    temp2, address2 = create_temp_variable('int')  # Assuming K is of 'int' type
    quadruples.append(('+', address1, K_address, address2))

    # # Generate quadruple for adding base virtual address
    # base_address = array_info['virtual_address']
    # temp3, address3 = create_temp_variable('int')  # Assuming the address result is of 'int' type
    # quadruples.append(('+', base_address, address2, address3))

    # Now, we need to dereference the address stored in address3
    # First, create a new temp variable to store the dereferenced value
    temp4, address4 = create_temp_variable(array_info['type'])  # the type should match the array's type

    # Generate a quadruple that fetches the value at the address stored in address3
    quadruples.append(('DEREF', address2, None, address4)) 

    # Push the dereferenced address to the operands_stack and types_stack
    operands_stack.append(address4)
    types_stack.append(array_info['type'])

# Function to validate the array befor initalization
def validate_array_initialization(array_declaration, initialization_list):
    #print(f"Array declaration: {array_declaration}")  # Debugging line
    array_id = array_declaration[1]
    array_size = array_declaration[2][0]['LSDIM'] + 1  # Extract LSDIM from the first dictionary in the list
    if len(initialization_list) - 1 != array_size:
        raise SyntaxError(f"Array '{array_id}' declared of size {array_size}, but initialized with {len(initialization_list)} values.")

# Function to validate the array before access
def validate_array_access(array_id, index):
    declare_constant(index, 'int')
    indx_address = get_memory_address(index)

    array_size = dir_func[current_scope[-1]]['local_variables'][array_id]['dimensions'][0]['LSDIM'] + 1
    if not 0 <= indx_address < array_size:
        raise SyntaxError(f"Index {index} out of bounds for array '{array_id}' of size {array_size}.")

#Function to initialize the array
def handle_array_initialization(array_declaration, initialization_list):
    global current_scope
    global dir_func
    global const_table
    array_id = array_declaration[1]  # Extract array id from the declaration
    array_type = array_declaration[3]

    array_info = dir_func[current_scope[-1]]['local_variables'][array_id]

    # Verify if the initialization list length matches the array size
    if len(initialization_list) != (array_info['size']):
        raise ValueError(f"Initialization size mismatch for array '{array_id}'.")

    LiDIM = 1
    last_value = len(initialization_list)
    LSDIM = last_value
    R = LSDIM - LiDIM + 1  # The range of the array
    mDIM = array_info['size'] / R
    K = -LiDIM * mDIM

    # Create the dimension node with the appropriate information
    dimension_node = {
        'LiDIM': LiDIM,
        'LSDIM': LSDIM,
        'DIM': 1,
        'mDIM': mDIM,
        'K': K
    }

    # Save the dimension node to the array information in the current function scope
    dir_func[current_scope[-1]]['local_variables'][array_id]['dimensions'] = [dimension_node]

    # Generate quadruples for each initialization value
    for i, value in enumerate(initialization_list):
        # Declare the constant and get its memory address
        declare_constant(value, array_type)
        address = get_memory_address(value)

        # Calculate the address for the current array element
        element_address = array_info['virtual_address'] + i

        # Generate the assignment quadruple
        quadruples.append(('=', address, None, element_address))
