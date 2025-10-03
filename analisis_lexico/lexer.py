from .tokens import Token
from .tabla_transicion import tabla_transicion
from .expr_reg import TOKEN_REGEX

tipo_dato = ["void", "int", "double", "string", "boolean", "char"]
palabras_reservadas = ["class", "void", "main", "if", "else", "while", "for", "return", "new", "print", "read", "int", "double", "string", "boolean", "char", "void", "continue", "break"]

class Lexer:
    def __init__(self, archivo):
        self.pos = 0
        self.linea = 1
        self.tokens = []
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                self.code = file.read()
        except (FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Error al leer archivo: {e}")
            
    def __str__(self):
        if not self.tokens: return "El Lexer no ha generado ningún token aún."
        
        lineas = []
        
        cabecera = f"{'ID':<5} {'Linea':<5} {'Tipo':<25} {'Lexema':<30}"
        separador = "-" * 65
        
        lineas.append(cabecera)
        lineas.append(separador)
        
        for token in self.tokens:
            valor_legible = repr(token.valor)[1:-1]

            fila = f"{token.id:<5} {token.linea:<5} {token.tipo:<25} {valor_legible:<30}"
            lineas.append(fila)
            
        return '\n'.join(lineas)
        
    def tokenize(self):
        self.pos = 0
        
        while self.pos < len(self.code):
            token: Token
            token = self.clasificar_token()
            if token:
                if token.id not in [101, 102]:
                    self.tokens.append(token) # Insertar nodo
            else: break
        return self.tokens
            
    # Clasifica tokens
    def clasificar_token(self):
        token: Token
        # char = ''
        tipo: str
        char = self.peek_char()
        
        if char is None:
            return None
        
        tipo = self.clasificar_char(char)
        
        # SALTO DE LINEA
        if tipo == "SALTO LINEA":
            self.linea += 1
            self.pos += 1
            return Token(102, tipo, char, self.linea, self.pos)
        
        # ESPACIO
        if tipo == "ESPACIO":
            self.pos += 1
            return Token(101, tipo, char, self.linea, self.pos)
        
        # IDENTIFICADOR, PALABRA RESERVADA O TIPO DE DATO
        if tipo in ["LETRA", "_"]:
            # IDENTIFICADOR
            # self.pos -= 1
            token = self.run_automata("IDENTIFICADOR")
            if token:
                # PALABRA RESERVADA O TIPO DE DATO
                if token[1] in palabras_reservadas:
                    regex = []
                    for token_id, token_type, token_value in TOKEN_REGEX:
                        if token_value == token[1]:
                            return Token(token_id, token_type, token_value, self.linea, self.pos) # ej: (22, INT, int, 1)
                else:
                    token_id = 31
                    token_type = "IDENTIFICADOR"
                    return Token(token_id, token_type,token[1], self.linea, self.pos)
            else:
                raise SyntaxError("ERROR: Identificador inválido")

        # NUMERO Ú OPERADOR MENOS
        elif tipo in ["OP MENOS", "DIGITO", "PUNTO"]:
            # NUMERO REAL
            token = self.run_automata("REAL")
            if token:
                return Token(32, token[0], token[1], self.linea, self.pos)
            # NUMERO ENTERO
            token = self.run_automata("ENTERO")
            if token:
                return Token(33, token[0], token[1], self.linea, self.pos)
            # OPERADOR MENOS (-)
            if tipo == "OP MENOS":
                self.pos += 1
                return Token(53, "OP RESTA", char, self.linea, self.pos)
            # PUNTO
            if tipo == "PUNTO":
                self.pos += 1
                return Token(93, tipo, char, self.linea, self.pos)
        
        # COMENTARIOS Ú OPERADOR DIVISIÓN
        elif tipo == "SLASH":
            
            # COMENTARIO DE LINEA
            token = self.run_automata("COMENTARIO LINEA")
            if token:
                return Token(41, token[0], token[1], self.linea, self.pos)
            # COMENTARIO DE BLOQUE
            token = self.run_automata("COMENTARIO BLOQUE")
            if token:
                return Token(42, token[0], token[1], self.linea, self.pos)
            # OPERADOR DIVISION
            self.pos += 1
            return Token(55, "OP DIVISION", char, self.linea, self.pos)
        
        # CADENA
        elif tipo == "COMILLA DOBLE":
            token = self.run_automata("CADENA")
            if token:
                return Token(35, token[0], token[1], self.linea, self.pos)
            else:
                raise SyntaxError("ERROR: Cadena mal formada")
        
        # CARACTER
        elif tipo == "COMILLA SIMPLE":
            token = self.run_automata("CARACTER")
            if token:
                return Token(36, token[0], token[1], self.linea, self.pos)
            else:
                raise SyntaxError("ERROR: Char mal formado")
        
        # SIMBOLOS DE AGRUPACIÓN
        # PARENTESIS
        # IZQUIERDO
        elif tipo == "PARENTESIS IZQ":
            self.pos += 1
            return Token(82, tipo, char, self.linea, self.pos)
        # DERECHO
        elif tipo == "PARENTESIS DER":
            self.pos += 1
            return Token(83, tipo, char, self.linea, self.pos)
        # CORCHETE
        # IZQUIERDO
        elif tipo == "CORCHETE IZQ":
            self.pos += 1
            return Token(84, tipo, char, self.linea, self.pos)
        # DERECHO
        elif tipo == "CORCHETE DER":
            self.pos += 1
            return Token(85, tipo, char, self.linea, self.pos)
        # LLAVE
        # IZQUIERDO
        elif tipo == "LLAVE IZQ":
            self.pos += 1
            return Token(86, tipo, char, self.linea, self.pos)
        # DERECHO
        elif tipo == "LLAVE DER":
            self.pos += 1
            return Token(87, tipo, char, self.linea, self.pos)
        
        # OPERADOR RELACIONAL Ó NOT Ó ASIGNACIÓN
        # OPERADOR MENOR Ó MENOR IGUAL
        elif tipo == "OP MENOR":
            return self.lex_operadores_relacionales(77, tipo, char, 75, "OP MENOR IGUAL")
        # OPERADOR MAYOR Ó MAYOR IGUAL
        elif tipo == "OP MAYOR":
            return self.lex_operadores_relacionales(76, tipo, char, 74, "OP MAYOR IGUAL")
        # OPERADOR DISTINTO Ó NOT
        elif tipo == "OP NOT":
            return self.lex_operadores_relacionales(64, tipo, char, 73, "OP DISTINTO")
        # OPERADOR IGUAL Ó ASIGNACIÓN
        elif tipo == "OP IGUAL":
            tipo = "OP ASIGNACION"
            return self.lex_operadores_relacionales(80, tipo, char, 72, "OP IGUAL")
        
        # OPERADOR LOGICO
        # OPERADOR AND
        elif tipo == "OP AMPER":
            return self.lex_operadores_logicos(62, "OP AND", char, "OP AMPER")
        # OPERADOR OR
        elif tipo == "OP PIPE":
            return self.lex_operadores_logicos(63, "OP OR", char, "OP PIPE")
        # OPERADOR NOT (YA HECHO)
        
        # OPERADOR ARITMETICO
        # OPERADOR SUMA
        elif tipo == "OP MAS":
            self.pos += 1
            return Token(52, "OP SUMA", char, self.linea, self.pos)
        # OPERADOR RESTA (YA HECHO)
        # OPERADOR MULTIPLICACIÓN
        elif tipo == "OP POR":
            self.pos += 1
            return Token(54, "OP MULTIPLICACION", char, self.linea, self.pos)
        # OPERADOR DIVISIÓN (YA HECHO)
        
        # COMA
        elif tipo == "COMA":
            self.pos += 1
            return Token(92, tipo, char, self.linea, self.pos)
        
        # FIN DE LINEA
        elif tipo == "PUNTO Y COMA":
            self.pos += 1
            return Token(94, "PUNTO Y COMA", char, self.linea, self.pos)
        
        else:
            raise SyntaxError("ERROR: Token desconocido")
    
    # OPERADORES RELACIONALES
    def lex_operadores_relacionales(self, id_char: int, tipo_char: str, char, id_lexema: int, tipo_lexema: str):
        next_char = self.peek_char(1)
        next_tipo = self.clasificar_char(next_char)
        if next_tipo == "OP IGUAL":
            self.pos += 2
            lexema = char + next_char
            return Token(id_lexema, tipo_lexema, lexema, self.linea, self.pos)
        self.pos += 1
        return Token(id_char, tipo_char, char, self.linea, self.pos)
    # OPERADORES LOGICOS CONJUNTOS (AND, OR)
    def lex_operadores_logicos(self, id_lexema: int, tipo_lexema:str, char, tipo: str):
        next_char = self.peek_char(1)
        next_tipo = self.clasificar_char(next_char)
        if next_tipo == tipo:
            self.pos += 2
            lexema = char + next_char
            return Token(id_lexema, tipo_lexema, lexema, self.linea, self.pos)
        else: 
            raise SyntaxError(f"ERROR: Operador {tipo_lexema} mal formado")
        
    def run_automata(self, tipo):
        if tipo not in tabla_transicion:
            raise ValueError("ERROR: Automata no reconocido")
        
        estado = tabla_transicion[tipo]["INICIO"]
        if not estado:
            raise ValueError("ERROR: Automata no tiene estado inicial")
        
        pos_inicial = self.pos
        lexema = ""
        char = self.get_next_char()
        
        
        
        while char:
            categoria = self.clasificar_char(char)

            if categoria in tabla_transicion[tipo][estado]:
                estado = tabla_transicion[tipo][estado][categoria]
                lexema += char
                char = self.get_next_char()
            else: break

        if estado in tabla_transicion[tipo]["FIN"]:
            self.pos -= 1
            return (tipo, lexema)
        
        self.pos = pos_inicial
        return None
        
    def get_next_char(self):
        char = self.code[self.pos]
        self.pos += 1
        return char
    
    def peek_char(self, offset=0):
        pos = self.pos + offset
        return self.code[pos] if pos < len(self.code) else None
    
    def clasificar_char(self, char):
        if char.isalpha():
            return "LETRA"
        elif char.isdigit():
            return "DIGITO"
        elif char == "_":
            return "_"
        elif char == "'":
            return "COMILLA SIMPLE"
        elif char == '"':
            return "COMILLA DOBLE"
        elif char == "+":
            return "OP MAS"
        elif char == "-":
            return "OP MENOS"
        elif char == "*":
            return "OP POR"
        elif char == "/":
            return "SLASH"
        elif char == "<":
            return "OP MENOR"
        elif char == ">":
            return "OP MAYOR"
        elif char == "&":
            return "OP AMPER"
        elif char == "|":
            return "OP PIPE"
        elif char == "!":
            return "OP NOT"
        elif char == "=":
            return "OP IGUAL"
        elif char == "(":
            return "PARENTESIS IZQ"
        elif char == ")":
            return "PARENTESIS DER"
        elif char == "[":
            return "CORCHETE IZQ"
        elif char == "]":
            return "CORCHETE DER"
        elif char == "{":
            return "LLAVE IZQ"
        elif char == "}":
            return "LLAVE DER"
        elif char == ",":
            return "COMA"
        elif char == ".":
            return "PUNTO"
        elif char == ";":
            return "PUNTO Y COMA"
        elif char == '\n':
            return "SALTO LINEA"
        elif char == ' ':
            return "ESPACIO"
        elif char == None:
            return "EOF"
        else:
            return "DESCONOCIDO"
        

code_path = './code.txt'
lexer = Lexer(code_path)
tokens = lexer.tokenize()

print(lexer)