import ply.lex as lex
import ply.yacc as yacc

# Define the tokens
tokens = (
    'NAME',
    'NUMBER',
    'PRINT',
    'SET',
)

# Define the regular expressions for each token
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER = r'\d+'

# Define the token for the PRINT keyword
def t_PRINT(t):
    r'print'
    return t

# Define the token for the SET keyword
def t_SET(t):
    r'set'
    return t

# Ignore whitespace, tabs, and newlines
t_ignore = ' \t\n'

# Error handling for unknown tokens
def t_error(t):
    print(f"Unknown token '{t.value}'")
    t.lexer.skip(1)

# Create the lexer
lexer = lex.lex()

# Define the parsing rules
def p_statement_assign(p):
    'statement : SET NAME NUMBER'
    p[0] = ('assign', p[2], p[3])

def p_statement_print(p):
    'statement : PRINT NAME'
    p[0] = ('print', p[2])

def p_error(p):
    print("Syntax error in input!")

# Create the parser
parser = yacc.yacc()

# Define the semantics of the language
variables = {}

def execute_command(command):
    if command[0] == 'assign':
        variables[command[1]] = int(command[2])
    elif command[0] == 'print':
        if command[1] in variables:
            print(variables[command[1]])
        else:
            print(f"Variable '{command[1]}' has not been assigned a value.")

def execute_program(program):
    for statement in program:
        execute_command(statement)

# Read the program from the file
with open('test.fla', 'r') as f:
    program_text = f.read()

# Parse the program
program = []
lexer.input(program_text)
for tok in lexer:
    if tok.type in ('SET', 'PRINT'):
        # Add a command to the program whenever we see a SET or PRINT token
        command = (tok.type.lower(), lexer.token().value)
        program.append(command)

# Execute the program
execute_program(program)
