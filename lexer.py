import ply.lex as lex

tokens = (
    'PROGRAM', 'VARIABLES',
    'INT', 'FLOAT', 'STRING', 'BOOL',
    'PRINT',
    'ID',  'CTEI', 'FLOAT_NUMBER', 'STRING_LITERAL',
    'TRUE', 'FALSE',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA', 'COLON', 'IF', 'ELSE', 'WHILE',
    'LESS_THAN', 'GREATER_THAN', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUAL_EQUAL', 'NOT_EQUAL', 'RETURN', 'VOID', 'MAIN', 'TEACH_SUM', 'TEACH_SUBSTRACTION', 'TEACH_MULTIPLICATION', 'TEACH_DIVISION', 'TEACH_IF', 'TEACH_WHILE', 'TEACH_FUNCTION_DECLARATION', 'TEACH_FUNCTION_CALL', 'AYUDA'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_COLON = r':'
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_EQUAL_EQUAL = r'=='
t_NOT_EQUAL = r'!='

t_ignore = ' \t'

keywords = {
    'Program': 'PROGRAM',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'Variables': 'VARIABLES',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'bool': 'BOOL',
    'while': 'WHILE',
    'return': 'RETURN',
    'void': 'VOID',
    'main': 'MAIN',
}


def t_TRUE(t):
    r'true'
    t.value = True
    return t

# And add a regular expression rule for the new token
def t_TEACH_SUM(t):
    r'teach_sum'
    return t
# And add a regular expression rule for the new token
def t_TEACH_SUBSTRACTION(t):
    r'teach_subtraction'
    return t
# And add a regular expression rule for the new token
def t_TEACH_MULTIPLICATION(t):
    r'teach_multiplication'
    return t
# And add a regular expression rule for the new token
def t_TEACH_TEACH_DIVISION(t):
    r'teach_division'
    return t
# And add a regular expression rule for the new token
def t_TEACH_IF(t):
    r'teach_if'
    return t
# And add a regular expression rule for the new token
def t_TEACH_WHILE(t):
    r'teach_while'
    return t
# And add a regular expression rule for the new token
def t_TEACH_FUNCTION_DECLARATION(t):
    r'teach_function_declaration'
    return t
# And add a regular expression rule for the new token
def t_TEACH_FUNCTION_CALL(t):
    r'teach_function_call'
    return t

# And add a regular expression rule for the new token
def t_AYUDA(t):
    r'ayuda'
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t


def t_FLOAT_NUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z]([a-zA-Z]|[0-9])*'
    t.type = keywords.get(t.value, 'ID')
    return t


def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove the quotes
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()
