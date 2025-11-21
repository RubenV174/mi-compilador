from analisis_lexico.lexer import Lexer
from analisis_sintactico.parser import Parser
from codigo_intermedio.generador_ci import Generador_CI

code_path = './code.txt'

lexer = Lexer(code_path)
tokens = lexer.tokenize()
print(lexer)

parser = Parser(tokens)
ast = parser.parse()
print(parser)

var = parser.semantic.variables
print(var)

genCI = Generador_CI()
polish = genCI.generar_lista(ast)
print(genCI)