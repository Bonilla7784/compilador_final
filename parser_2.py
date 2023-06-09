import sys
import ply.yacc as yacc
from lexer import tokens
import traceback
from semantics import *
from obj_gen import generate_obj_file

temp_variable_counter = 0
main_start_index = None
function_table = {}


def create_scope(scope_name, return_type=None):
    '''Create a new scope.'''
    global current_scope
    # Add scope to the stack
    current_scope.append(scope_name)
    if return_type is not None:
        # Create a new symbol table for this scope in dir_func
        dir_func[scope_name] = {'local_variables': {}, 'param_list': [], 'start_quad': len(quadruples), 'num_params': 0, 'return_type': return_type, 'return_var': ''}
    else:
        # Create a new symbol table for this scope in dir_func
        dir_func[scope_name] = {'local_variables': {}, 'param_list': [], 'start_quad': len(quadruples), 'num_params': 0}

def end_scope():
    '''End the current scope.'''
    global current_scope
    # Remove the current scope from the stack

def p_program(p):
    '''program : PROGRAM ID SEMICOLON placeholder_goto_main create_scopes global_scope main_function end_scopes fill_goto_main'''
    p[0] = ('program', p[2], p[4], p[5], p[6], p[7])

def p_placeholder_goto_main(p):
    '''placeholder_goto_main : '''
    # Add a placeholder for the GOTO MAIN quadruple. This will be replaced later.
    quadruples.append(('Goto', None, None, None))
    
# Add function_decl_list to the global scope and main function
def p_global_scope(p):
    '''global_scope : VARIABLES LBRACE decl_list RBRACE function_decl_list
                    | VARIABLES LBRACE decl_list RBRACE'''
    #print('In global')
    if len(p) == 6:
        p[0] = ('global_scope', p[3], p[5])
    elif len(p) == 5:
        p[0] = ('global_scope', p[3], [])

def p_function_decl_list(p):
    '''function_decl_list : function_decl function_decl_list
                          | empty'''
    #print('In p_function_decl_list')
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_main_function(p):
    '''main_function : MAIN LPAREN RPAREN LBRACE start_main stmt_list RBRACE'''
    p[0] = ('main', p[6])

def p_start_main(p):
    '''start_main : '''
    # Mark the starting point of the main function. This will be the target of the GOTO MAIN quadruple.
    global main_start_index
    # Save the quadruple index where the main function starts
    main_start_index = len(quadruples)

def p_fill_goto_main(p):
    '''fill_goto_main : '''
    # Replace the placeholder GOTO MAIN quadruple.
    quadruples[0] = ('Goto', None, None, main_start_index)


def p_create_scopes(p):
    '''create_scopes : '''
    create_scope('global')

def p_end_scopes(p):
    '''end_scopes : '''
    
    end_scope()

def p_decl_list(p):
    '''decl_list : decl SEMICOLON decl_list
                 | decl SEMICOLON
                 | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_decl(p):
    '''decl : type ID
            | array_decl'''
    if len(p) == 3:
        add_to_current_scope(p[2], p[1], should_declare=True)
        p[0] = ('decl', p[1], p[2])
    else:
        p[0] = p[1]

def p_type(p):
    '''type : INT
            | FLOAT
            | STRING
            | BOOL'''
    #print('In type')
    p[0] = p[1]

def p_stmt_list(p):
    '''stmt_list : stmt SEMICOLON stmt_list
                 | stmt SEMICOLON'''
    #print('In stmt_list')
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_stmt(p):
    '''stmt : assign
            | array_assign
            | print
            | conditional
            | loop
            | function_call
            | decl
            | built_in_function
            | return_stmt'''
    p[0] = p[1]

def p_built_in_function(p):
    '''built_in_function : TEACH_SUM LPAREN RPAREN
                         | TEACH_SUBSTRACTION LPAREN RPAREN
                         | TEACH_MULTIPLICATION LPAREN RPAREN
                         | TEACH_DIVISION LPAREN RPAREN
                         | TEACH_IF LPAREN RPAREN
                         | TEACH_WHILE LPAREN RPAREN
                         | TEACH_FUNCTION_DECLARATION LPAREN RPAREN
                         | TEACH_FUNCTION_CALL LPAREN RPAREN
                         | AYUDA LPAREN RPAREN'''
    p[0] = ('built_in_function', p[1])
    generate_built_in_function_call(p[1])  # Generate a quadruple for the built-in function call

def generate_built_in_function_call(function_name):
    '''Generate a quadruple for a built-in function call.'''
    quadruples.append(('BUILTIN_FUNC', function_name, None, None))


def p_assign(p):
    '''assign : ID EQUALS expr'''
    #print('assign', p[1])
    id_type = get_variable_type(p[1])
    if id_type is None:
        raise Exception("Variable " + p[1] + " not declared")
    expr_type = types_stack.pop()
    if expr_type in semantic_cube['='][id_type] and semantic_cube['='][id_type][expr_type] is not None:
        operand = operands_stack.pop()
        generate_quadruple('=', operand, None, p[1])
    else:
        raise Exception("Type mismatch in assignment")

def p_expr(p):
    '''expr : expr PLUS term
            | expr MINUS term
            | expr comp_op term
            | term'''
    if len(p) == 4:
        right_type = types_stack.pop()
        left_type = types_stack.pop()
        operator = p[2]
        if semantic_cube[operator][left_type][right_type] is not None:
            result_type = semantic_cube[operator][left_type][right_type]
            right_operand = operands_stack.pop()
            left_operand = operands_stack.pop()
            temp_variable, temp_address = create_temp_variable(result_type)
            generate_quadruple(operator, left_operand, right_operand, temp_address)
            operands_stack.append(temp_address)
            types_stack.append(result_type)
            p[0] = temp_address  
        else:
            raise Exception("Type mismatch in expression")
    else:
        p[0] = p[1]



def p_term(p):
    '''term : term MULTIPLY factor
            | term DIVIDE factor
            | factor
            | function_call
            | array_access'''
    if len(p) == 4:
        right_type = types_stack.pop()
        left_type = types_stack.pop()
        operator = p[2]
        if semantic_cube[operator][left_type][right_type] is not None:
            result_type = semantic_cube[operator][left_type][right_type]
            right_operand = operands_stack.pop()
            left_operand = operands_stack.pop()
            temp_variable, temp_address = create_temp_variable(result_type)
            generate_quadruple(operator, left_operand,
                               right_operand, temp_address)
            operands_stack.append(temp_address)
            types_stack.append(result_type)
            p[0] = temp_address 
        else:
            raise Exception("Type mismatch in term")
    else:
        p[0] = p[1]


def p_factor(p):
    '''factor : LPAREN expr RPAREN
              | CTEI
              | FLOAT_NUMBER
              | STRING_LITERAL
              | TRUE
              | FALSE
              | ID
              | function_call'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        if isinstance(p[1], bool):
            declare_constant(p[1], 'bool')
            operands_stack.append(get_memory_address(p[1]))
            types_stack.append('bool')
            p[0] = p[1]  # Assign memory address to p[0]
        elif isinstance(p[1], int):
            declare_constant(p[1], 'int')
            operands_stack.append(get_memory_address(p[1]))
            types_stack.append('int')
            p[0] = p[1]  # Assign memory address to p[0]
        elif isinstance(p[1], float):
            declare_constant(p[1], 'float')
            operands_stack.append(get_memory_address(p[1]))
            types_stack.append('float')
            p[0] = p[1]  # Assign memory address to p[0]
        elif isinstance(p[1], str):
            # Check if the string is a variable identifier
            var_type = get_variable_type(p[1])
            if var_type is not None:  # The string is a variable identifier
                operands_stack.append(get_memory_address(p[1]))
                types_stack.append(var_type)
                p[0] = p[1]  # Assign memory address to p[0]
            else:  # The string is a string literal
                declare_constant(p[1], 'string')
                operands_stack.append(get_memory_address(p[1]))
                types_stack.append('string')
                p[0] = p[1]  # Assign memory address to p[0]
        else:
            raise Exception("Variable " + p[1] + " not declared")



def p_print(p):
    '''print : PRINT COLON expr
             | PRINT COLON expr COMMA expr'''
    generate_quadruple('print', None, None, p[3])


def p_conditional(p):
    '''conditional : IF LPAREN comp_expr RPAREN LBRACE stmt_list RBRACE else_stmt
                   | IF LPAREN comp_expr RPAREN LBRACE stmt_list RBRACE'''
    if len(p) == 9:
        p[0] = ('if', p[3], p[6], p[8])
        end_else()  # Here, we make sure that end_else() is called after both the 'if' and 'else' parts are parsed
    else:
        p[0] = ('if', p[3], p[6])
        end_if()  # If there's no 'else' part, we can simply call end_if() here


def p_comp_expr(p):
    '''comp_expr : expr comp_op expr'''
    right_type = types_stack.pop()
    left_type = types_stack.pop()
    operator = operators_stack.pop()
    if semantic_cube[operator][left_type][right_type] is not None:
        result_type = semantic_cube[operator][left_type][right_type]
        right_operand = operands_stack.pop()
        left_operand = operands_stack.pop()
        temp_variable, temp_address = create_temp_variable(result_type)
        quadruple = generate_quadruple(
            operator, left_operand, right_operand, temp_address)
        operands_stack.append(temp_address)
        types_stack.append(result_type)
        # Call start_if here after generating comparison quadruple
        start_if(temp_address)
    else:
        raise Exception("Type mismatch in comparison expression")
    p[0] = ('comp_expr', p[1], p[2], p[3])


def p_comp_op(p):
    '''comp_op : LESS_THAN
               | GREATER_THAN
               | LESS_EQUAL
               | GREATER_EQUAL
               | EQUAL_EQUAL
               | NOT_EQUAL'''
    operators_stack.append(p[1])
    p[0] = p[1]


def p_else_stmt(p):
    '''else_stmt : ELSE LBRACE else_part stmt_list RBRACE
                 | empty'''
    if len(p) == 6:
        p[0] = ('else', p[4])
    else:
        p[0] = None
        end_if()


def p_else_part(p):
    '''else_part : '''
    else_part()


def p_loop(p):
    '''loop : WHILE LPAREN comp_expr RPAREN LBRACE stmt_list RBRACE'''
    start_while()  # Start while before evaluating the condition expression
    p[3] = ('while', p[3], p[6])
    end_while()
    p[0] = p[3]

def p_create_function_scope(p):
    '''create_function_scope : '''
    func_name = p[-2]  # function name
    if func_name in dir_func:
        raise Exception(f"Function {func_name} already declared.")
    create_scope(func_name, p[-3])  # creates a new scope using the function name as the scope name

def p_function_decl(p):
    '''function_decl : type ID LPAREN create_function_scope param_list RPAREN LBRACE stmt_list end_scopes RBRACE
                     | VOID ID LPAREN create_function_scope param_list RPAREN LBRACE stmt_list_without_return end_scopes RBRACE'''

    global current_function
    current_function = p[2]  # Start the function's local scope
    if p[1] == 'void':
        p[0] = ('function_decl', 'void', current_function, p[5], p[7])
        handle_function_declaration(current_function, p[5], p[7], 'void')  
    else:  # non-void function
        p[0] = ('function_decl', p[1], current_function, p[5], p[7], p[7])
        handle_function_declaration(current_function, p[5], p[7], p[1])  

    quadruples.append(('ENDfunc', None, None, None))


def p_stmt_list_without_return(p):
    '''stmt_list_without_return : stmt_without_return SEMICOLON stmt_list_without_return
                 | stmt_without_return SEMICOLON'''
    #print('In stmt_list')
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_stmt_without_return(p):
    '''stmt_without_return : assign
            | array_assign
            | print
            | conditional_without_return
            | loop
            | function_call
            | decl
            | built_in_function'''
    #print('In stmt')
    p[0] = p[1]    

def p_conditional_without_return(p):
    '''conditional_without_return : IF LPAREN comp_expr RPAREN LBRACE stmt_list_without_return RBRACE else_stmt
                   | IF LPAREN comp_expr RPAREN LBRACE stmt_list_without_return RBRACE'''
    if len(p) == 9:
        p[0] = ('if', p[3], p[6], p[8])
        end_else()  # Here, we make sure that end_else() is called after both the 'if' and 'else' parts are parsed
    else:
        p[0] = ('if', p[3], p[6])
        end_if()  # If there's no 'else' part, we can simply call end_if() here

def p_return_stmt(p):
    '''return_stmt : RETURN expr'''
    if len(p) == 3:
        p[0] = ('return_stmt', p[2])
        global current_function
        current_function = current_scope[-1]  # Use the last scope added as the current function
        #print(current_function)
        if p[2] not in dir_func[current_function]['local_variables']:
            raise Exception(f"Return variable {p[2]} not found in function {current_function}.")
        handle_function_return(p[2], current_function)

def p_function_call(p):
    '''function_call : ID LPAREN arg_list RPAREN'''
    function_name = p[1]
    arg_list = p[3]
    p[0] = ('function_call', function_name, arg_list)
    handle_function_call(function_name, arg_list)

def p_arg_list(p):
    '''arg_list : arg_list COMMA expr
                | expr'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_param_list(p):
    '''param_list : param COMMA param_list
                  | param
                  | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_param(p):
    '''param : type ID'''
    p[0] = ('param', p[1], p[2])
    # add_to_current_scope(p[2], p[1], should_declare=True)
    declare_param_variable(p[2], p[1])

def add_to_current_scope(var_name, var_type, is_temp=False, should_declare=False):
    '''Add a variable to the current scope.'''
    global current_scope
    #print(var_name, var_type)
    if should_declare:
        declare_variable(var_name, var_type)
    #print(dir_func)

# Array declaration
def p_array_decl(p):
    '''array_decl : type ID LBRACKET CTEI RBRACKET'''
    #print('In array_decl', p[4])
    # dimensions = [(0, p[4] - 1)]  # Assuming zero-based array
    declare_array(p[2], p[1], p[4])  # Store array in symbol table
    p[0] = ('array_decl', p[2], p[4], p[1])

# Array assignment after declaration
def p_array_assign(p):
    '''array_assign : ID EQUALS LBRACE CTEI_list RBRACE '''
    # p[1] refers to array ID
    # p[4] refers to a list of values

    array_size = dir_func[current_scope[-1]]['local_variables'][p[1]]['size']
    array_type = dir_func[current_scope[-1]]['local_variables'][p[1]]['type']

    array_decl = ('array_decl', p[1], array_size, array_type)

    # validate_array_initialization(array_decl, p[4])
    handle_array_initialization(array_decl, p[4])

    p[0] = ('array_assign', array_decl, p[4])

def p_CTEI_list(p):
    '''CTEI_list : CTEI
                | CTEI_list COMMA CTEI'''
    if len(p) == 2:  # Single constant
        p[0] = [p[1]]
    else:  # Constant list
        p[0] = p[1] + [p[3]]


def p_array_access(p):
    '''array_access : ID LBRACKET expr RBRACKET'''
    # p[1] is the array ID
    # p[3] is the index expression
    #print('Array access', p[1], p[3])
    # validate_array_access(p[1], p[3])
    p[0] = handle_array_access(p[1], p[3])  # Assuming this function generates required quadruples for access and returns the final address

def p_empty(p):
    '''empty :'''
    p[0] = []


def p_error(p):
    if p:
        print(
            f"Syntax error at '{p.value}', line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at EOF")


yacc.yacc()

def parse(filename):
        if len(sys.argv) > 1:
            file = sys.argv[1]
            try:
                with open(file, 'r') as f:
                    data = f.read()
                    result = yacc.parse(data)
                    if result is not None:
                        print("Compilacion terminada correctamente.")
                        # END program
                        quadruples.append(('End', None, None, None))
                        #add_goto_main_quadruple()  # Call the function here
                        #print(result)  # Imprimir el resultado
                        print_quadruples()  # Imprimir los quadruples
                        #print(dir_func)
                        generate_obj_file(file + '.obj', dir_func, const_table, quadruples)
                    elif result:
                        print(result)
            except FileNotFoundError:
                print("Error: file not found")
            except Exception as e:
                print(f"Error: {e}")
                print(f"Exception type: {type(e).__name__}")
                traceback.print_tb(e.__traceback__)
                print("Syntax error occurred.")
        else:
            print("No se encontro archivo.")
