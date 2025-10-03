from analisis_lexico.lexer import Lexer

code_path = './code.txt'

lexer = Lexer(code_path)
tokens = lexer.tokenize() # Lista de tokens
print(lexer) # Imprime lista de tokens