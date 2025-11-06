from analisis_lexico.lexer import Lexer
from analisis_sintactico.parser import Parser
from codigo_intermedio.generador_ci import Generador_CI

code_path = './code.txt'

lexer = Lexer(code_path)
tokens = lexer.tokenize() # Genera Lista de Tokens
print(lexer)

parser = Parser(tokens)
ast = parser.parse() # Genera AST y Lista de Variables
print(parser)

var = parser.semantic.variables
print(var)

genCI = Generador_CI()
polish = genCI.generar_lista(ast)
print(polish)