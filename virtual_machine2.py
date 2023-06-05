import json
class Memory:
    def __init__(self, start_addresses):
        self.memory = {}
        self.next_addresses = start_addresses.copy()

    def get(self, address):
        #print(f'Getting value at memory address {address}')
        return self.memory.get(address)

    def set(self, address, value):
        #print(f'Setting memory address {address} to value {value}')
        self.memory[address] = value

    def assign(self, var_type):
        address = self.next_addresses[var_type]
        self.next_addresses[var_type] += 1
        return address


class GlobalMemory(Memory):
    pass


class TempMemory(Memory):
    pass


class LocalMemory(Memory):
    pass


class ExecutionStack:
    def __init__(self):
        self.stack = []

    def push(self, context):
        self.stack.append(context)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        if len(self.stack) > 0:
         return self.stack[-1]
        else:
            return None

local_memory = LocalMemory({
    'int': 7000,
    'float': 8000,
    'bool': 9000,
    'string': 10000,
    'temp': 11000
})

class ExecutionContext:
    def __init__(self, return_address, start_addresses):
        self.local_memory = LocalMemory(start_addresses)
        self.return_address = return_address


def load_obj_file(filename):
    with open(filename, 'r') as file:
        obj_file = json.load(file)
    return obj_file['DirFunc'], obj_file['ConstTable'], obj_file['Quadruples']


def initialize_memory(dir_func, const_table, global_memory, const_memory):
    # Initialize constants
    for const_value, const_attributes in const_table.items():
        try:
            if '.' in const_value:
                const_value = float(const_value)
            else:
                const_value = int(const_value)
        except ValueError:
            pass

        const_memory.set(const_attributes['memory_address'], const_value)

def get_local_address_for_param(dir_func, param_number, current_function):
    function_info = dir_func[current_function]
    param_info = function_info['param_list'][param_number]
    return param_info[2]  # Return the memory address of the parameter

def teach_sum():
    print("La suma de dos números 'a' y 'b' se puede calcular con el operador '+': 'a + b'.")

def teach_subtraction():
    print("La diferencia de dos números 'a' y 'b' se puede calcular con el operador '-': 'a - b'.")

def teach_multiplication():
    print("El producto de dos números 'a' y 'b' se puede calcular con el operador '*': 'a * b'.")

def teach_division():
    print("El cociente de dos números 'a' y 'b' se puede calcular con el operador '/': 'a / b'. Nota: 'b' no debe ser cero.")

def teach_if():
    print("Una sentencia if te permite ejecutar código de manera condicional. La sintaxis es 'if (condición) { // código a ejecutar si la condición es verdadera }'. La condición debe ser una expresión booleana.")

def teach_while():
    print("Un bucle while ejecuta repetidamente un bloque de código mientras una condición sea verdadera. La sintaxis es 'while (condición) { // código a ejecutar mientras la condición es verdadera }'.")

def teach_function_declaration():
    print("Puedes declarar una función usando la sintaxis 'function nombreFuncion() { // código }'. Esto crea un bloque de código reutilizable que puede ser llamado por el nombre de la función.")

def teach_function_call():
    print("Una vez que una función ha sido declarada, puedes llamarla por su nombre seguido de paréntesis: 'nombreFuncion()'. Si la función toma parámetros, puedes pasarlos en los paréntesis.")

def ayuda():
    print("Estas son todas las funciones de 'enseñanza' que puedes usar:")
    for function_name in built_in_functions.keys():
        if function_name.startswith('teach_'):
            print(f"- {function_name}")


# Mapping of built-in function names to their implementations
built_in_functions = {
    'teach_sum': teach_sum,
    'teach_substraction': teach_subtraction,
    'teach_multiplication': teach_multiplication,
    'teach_division': teach_division,
    'teach_if': teach_if,
    'teach_while': teach_while,
    'teach_function_declaration': teach_function_declaration,
    'teach_function_call': teach_function_call,
    'ayuda': ayuda
}

def execute_built_in_function(function_name):
    '''Execute a built-in function.'''
    if function_name in built_in_functions:
        # Call the function
        built_in_functions[function_name]()
    else:
        raise Exception(f"Unknown built-in function '{function_name}'")
    
def execute_quadruples(quadruples, dir_func, const_table, global_memory, temp_memory, const_memory, execution_stack):
    IP = 0
    current_function = "global"  # Initialize current_function to "global"
    while IP < len(quadruples):
        operation, operand1, operand2, result = quadruples[IP]
        #print(operation, operand1, operand2, result)
        if operation == 'BUILTIN_FUNC':
            execute_built_in_function(operand1)
        if operation in ["+", "-", "*", "/"]:
            operand1_value = None
            operand2_value = None

            if operand1_value is None:
                operand1_value = global_memory.get(operand1)
                if operand1_value is None:
                    operand1_value = const_memory.get(operand1)
                    if operand1_value is None:
                        operand1_value = temp_memory.get(operand1)

            if operand2_value is None:
                operand2_value = global_memory.get(operand2)
                if operand2_value is None:
                    operand2_value = const_memory.get(operand2)
                    if operand2_value is None:
                        operand2_value = temp_memory.get(operand2)

            if operand1_value is None:
                operand1_value = execution_stack.peek().local_memory.get(operand1)
            if operand2_value is None:
                operand2_value = execution_stack.peek().local_memory.get(operand2)

            if operation == "+":
                temp_memory.set(result, operand1_value + operand2_value)
            elif operation == "-":
                temp_memory.set(result, operand1_value - operand2_value)
            elif operation == "*":
                temp_memory.set(result, operand1_value * operand2_value)
            elif operation == "/":
                temp_memory.set(result, operand1_value / operand2_value)

        elif operation in ["==", "!=", "<", ">", "<=", ">="]:
            operand1_value = None
            operand2_value = None

            if operand1_value is None:
                operand1_value = global_memory.get(operand1)
                if operand1_value is None:
                    operand1_value = const_memory.get(operand1)
                    if operand1_value is None:
                        operand1_value = temp_memory.get(operand1)

            if operand2_value is None:
                operand2_value = global_memory.get(operand2)
                if operand2_value is None:
                    operand2_value = const_memory.get(operand2)
                    if operand2_value is None:
                        operand2_value = temp_memory.get(operand2)

            if operand1_value is None:
                operand1_value = execution_stack.peek().local_memory.get(operand1)
            if operand2_value is None:
                operand2_value = execution_stack.peek().local_memory.get(operand2)

            if operation == "==":
                temp_memory.set(result, operand1_value == operand2_value)
            elif operation == "!=":
                temp_memory.set(result, operand1_value != operand2_value)
            elif operation == "<":
                temp_memory.set(result, operand1_value < operand2_value)
            elif operation == ">":
                temp_memory.set(result, operand1_value > operand2_value)
            elif operation == "<=":
                temp_memory.set(result, operand1_value <= operand2_value)
            elif operation == ">=":
                temp_memory.set(result, operand1_value >= operand2_value)

        elif operation == "GotoF":

            operand1_value = global_memory.get(operand1) or temp_memory.get(operand1)
            if not operand1_value:
                IP = result - 1

        elif operation == "Goto":
            IP = result - 1 
        elif operation == "=":
            execution_context = execution_stack.peek()
            value_to_assign = execution_context.local_memory.get(operand1) if execution_context is not None else None

            if value_to_assign is None:
                value_to_assign = const_memory.get(operand1)
                if value_to_assign is None:
                    value_to_assign = global_memory.get(operand1)
                    if value_to_assign is None:
                        value_to_assign = temp_memory.get(operand1)

            global_memory.set(result, value_to_assign)

        elif operation == "ASSIGN":
            # Get the return value (stored in temporary memory during the RETURN operation)
            execution_context = execution_stack.peek()
            value_to_assign = execution_context.local_memory.get(operand1) if execution_context is not None else None

            if value_to_assign is None:
                value_to_assign = const_memory.get(operand1)
                if value_to_assign is None:
                    value_to_assign = global_memory.get(operand1)
                    if value_to_assign is None:
                        value_to_assign = temp_memory.get(operand1)
            # Assign return value to the return variable (result)
            temp_memory.set(result, value_to_assign)

        elif operation == "print":
            print_value = global_memory.get(result)
            print(print_value)

        elif operation == "ERA":
            # Save current context and create a new one for the function call
            return_address = IP
            start_addresses = {'int': 7000, 'float': 8000, 'bool': 9000, 'string': 10000, 'temp': 11000}
            execution_stack.push(ExecutionContext(return_address, start_addresses))
            current_function = operand1

        elif operation == "GOSUB":
            # Save the return address
            return_address = IP + 1 

            # Change the IP to the start of the function
            IP = result - 1

            # Set the return address in the current execution context
            execution_stack.peek().return_address = return_address


        elif operation == "PARAMETER":
            # Get value to pass as parameter
            param_value = execution_stack.peek().local_memory.get(operand1)
            if param_value is None:
                param_value = const_memory.get(operand1)
                if param_value is None:
                    param_value = global_memory.get(operand1)
                    if param_value is None:
                        param_value = temp_memory.get(operand1)
            # Get the local address for the parameter in the current function
            param_local_address = get_local_address_for_param(dir_func, result, current_function)
            # Assign parameter value to the corresponding local memory address
            execution_stack.peek().local_memory.set(param_local_address, param_value)

        elif operation == "RETURN":
            # Try to get the operands from the local memory of the current execution context
            return_value = execution_stack.peek().local_memory.get(result)
            # Get value to return
            if return_value is None:
                return_value = const_memory.get(result)
                if return_value is None:
                    return_value = global_memory.get(result)
                    if return_value is None:
                        return_value = temp_memory.get(result)
            # Assign return value to the return variable (result)
            global_memory.set(result, return_value)

        elif operation == "ENDfunc":
            # Restore previous execution context
            if execution_stack.stack:
                context = execution_stack.pop()
                IP = context.return_address - 1
                if len(execution_stack.stack) > 0:
                    # If there are still functions on the stack, set current_function to the function on top of the stack
                    current_function = execution_stack.peek().function_name
            else:
                # If the stack is empty, we're back in the global scope
                current_function = "global"

        elif operation == "End":
            break

        IP += 1

    return global_memory.memory

def execute(obj_filename):
    dir_func, const_table, quadruples = load_obj_file('factorial_test.txt.obj')

    global_memory = GlobalMemory({
        'int': 1000,
        'float': 2000,
        'bool': 3000,
        'string': 4000,
        'temp': 5000,
        'const': 6000
    })
    

    temp_memory = TempMemory({
        'int': 12000,
        'float': 13000,
        'bool': 14000,
        'string': 15000
    })

    const_memory = Memory({
        'const': 6000
    })

    execution_stack = ExecutionStack()

    initialize_memory(dir_func, const_table, global_memory, const_memory)

    final_memory_state = execute_quadruples(quadruples, dir_func, const_table, global_memory, temp_memory, const_memory, execution_stack)
