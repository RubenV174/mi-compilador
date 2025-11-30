from analisis_lexico.lexer import Lexer
from analisis_sintactico.parser import Parser
from codigo_intermedio.generador_ci import Generador_CI

def leer_archivo(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        raise e(f"Error al leer archivo: {e}")

if __name__ == "__main__":
    path = './code.txt'
    codigo_fuente = leer_archivo(path)

    lexer = Lexer(codigo_fuente)
    tokens = lexer.tokenize()
    print(lexer)

    parser = Parser(tokens)
    ast = parser.parse()
    print(parser)

    var = parser.semantic.variables
    print(var)

    genCI = Generador_CI(ast)
    polish = genCI.generar_lista()
    print(genCI)