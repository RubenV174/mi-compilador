from analisis_lexico.lexer import Lexer
from analisis_sintactico.parser import Parser

code_path = './code.txt'

lexer = Lexer(code_path)
tokens = lexer.tokenize() # Genera Lista de Tokens
print(lexer)

parser = Parser(tokens)
parser.parse() # Genera AST y Lista de Variables
print(parser)

var = parser.semantic.variables
print(var)