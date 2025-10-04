from .ASTNode import AST
from analisis_lexico.lexer import Lexer
from analisis_lexico.expr_reg import TOKEN_REGEX
from analisis_lexico.tokens import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        
        self.pos = 0
        
        self.token_actual: Token = self.tokens[0] if tokens else None
        
        self.ast: AST
        
    def __str__(self):
        if not self.ast: return "El Parser aún no ha generado un AST"
        
        lineas = ["Árbol Sintáctico Abstracto"]
        
        self._generar_str_ast(self.ast, lineas)
        lineas.append("------------------------")
        
        return '\n'.join(lineas)
    
    def _generar_str_ast(self, nodo, lineas, nivel=0):
        if nodo is None: return
        
        identacion = "    " * nivel
        valor = f": {nodo.valor}" if nodo.valor is not None else ""
        
        lineas.append(f"{identacion}└── {nodo.tipo}{valor}")
        
        for hijo in nodo.hijos:
            self._generar_str_ast(hijo, lineas, nivel + 1)
            
    def __repr__(self):
        num_tokens = len(self.tokens)
        status = "Parseado" if self.ast else "No parseado"
        return f'<Parser status="{status}" num_tokens={num_tokens}>'
        
    def avanzar(self):
        self.pos += 1
        self.token_actual = self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def peek(self, offset=1):
        pos_peek = self.pos + offset
        return self.tokens[pos_peek] if pos_peek < len(self.tokens) else None
            
    def match(self, tipo_esperado):
        if tipo_esperado == "TIPO DATO":
            return self.token_actual and self.token_actual.valor in ["void", "int", "double", "string", "char", "boolean"]
        return self.token_actual and self.token_actual.tipo == tipo_esperado
    
    def consumir(self, tipo_esperado):
        if self.match(tipo_esperado):
            token = self.token_actual
            self.avanzar()
            return token
        else:
            print(f"Error Semántico: Se esperaba '{tipo_esperado}' pero se encontró '{self.token_actual.tipo}' en línea {self.token_actual.linea}")
            return None
            
    def parse(self):
        self.ast = self.parse_programa()
        if self.token_actual:
            print(f"Error Sintáctico: Tokens inesperados despues del cierre de clase: '{self.token_actual.valor}'")
            return None
        return self.ast
    
    def parse_programa(self):
        self.consumir("CLASS")
        nombre = self.consumir("IDENTIFICADOR")
        self.consumir("LLAVE IZQ")
        miembros = self.parse_miembros()
        self.consumir("LLAVE DER")
        return AST("PROGRAMA", valor=nombre.valor, hijos=miembros)
    
    def parse_miembros(self):
        miembros = []
        while self.token_actual and self.token_actual.tipo != 'LLAVE DER':
            miembros.append(self.parse_miembro())
        return miembros
    
    def parse_miembro(self):
        tipo = self.consumir("TIPO DATO")
        
        nombre = None
        if self.match("IDENTIFICADOR") or self.match("MAIN"):
            nombre = self.token_actual
            self.avanzar()
        else: 
            print(f"Error Semántico: Se esperaba un identificador o 'main' después del tipo de dato en la línea {self.token_actual.linea}")
            return None
        
        if self.match("PARENTESIS IZQ"):
            return self.parse_metodo(tipo.valor, nombre.valor)
        else:
            return self.parse_declaracion_variable(tipo.valor, nombre)
        
    def parse_metodo(self, tipo, nombre):
        self.consumir("PARENTESIS IZQ")
        parametros = self.parse_parametros()
        self.consumir("PARENTESIS DER")
        self.consumir("LLAVE IZQ")
        cuerpo = self.parse_sentencias()
        self.consumir("LLAVE DER")
        return AST(
            "METODO",
            valor=nombre,
            hijos=[
                AST("TIPO DATO", valor=tipo),
                AST("PARAMETROS", hijos=parametros),
                AST("CUERPO", hijos=cuerpo)
            ]
        )
    
    def parse_parametros(self):
        parametros = []
        if self.match("PARENTESIS DER"): return parametros
        while True:
            tipo = self.consumir("TIPO DATO")
            nombre = self.consumir("IDENTIFICADOR")
            parametro = AST(
                tipo="PARAMETRO",
                hijos=[
                    AST("TIPO DATO", valor=tipo.valor),
                    AST("IDENTIFICADOR", valor=nombre.valor)
                ]
            )
            parametros.append(parametro)
            if self.match("COMA"): break
            self.consumir("COMA")
        return parametros
    
    def parse_sentencias(self):
        sentencias = []
        while self.token_actual and not self.match("LLAVE DER"):
            sentencias.append(self.parse_sentencia())        
        return sentencias
    
    def parse_sentencia(self):
        if self.match("TIPO DATO"): return self.parse_declaracion_variable()
        elif self.match("IF"): return self.parse_if()
        elif self.match("WHILE"): return self.parse_while()
        elif self.match("FOR"): return self.parse_for()
        elif self.match("RETURN"): return self.parse_return()
        elif self.match("PRINT"): return self.parse_print()
        elif self.match("READ"): return self.parse_read()
        elif self.match("BREAK"): return self.parse_break()
        elif self.match("CONTINUE"): return self.parse_continue()
        elif self.match("IDENTIFICADOR"):
            if self.peek() and self.peek().tipo == "OP ASIGNACION":
                return self.parse_asignacion()
            elif self.peek() and self.peek().tipo == "PARENTESIS IZQ":
                return self.parse_llamada_funcion()
        print(f"Sentencia inválida en linea {self.token_actual.linea}, token: {self.token_actual.valor}")
        return None

    
    def parse_declaracion_variable(self, tipo_consumido=None, primer_identificador=None):
        tipo = tipo_consumido or self.consumir("TIPO DATO").valor
        declaraciones = []
        
        while True:
            identificador = primer_identificador or self.consumir("IDENTIFICADOR")
            primer_identificador = None
            
            expresion_hijo = None
            if self.match("OP ASIGNACION"):
                self.consumir("OP ASIGNACION")
                expresion_hijo = self.parse_expresion()
                
            declaraciones.append(
                AST(
                    "DECLARACION",
                    valor=identificador.valor,
                    hijos=[AST(
                        "TIPO",
                        valor=tipo
                    ), expresion_hijo]
                )
            )
            
            if not self.match("COMA"): break
            self.consumir("COMA")
        
        self.consumir("PUNTO Y COMA")
        return AST("LISTA DECLARACIONES", hijos=declaraciones)
    
    def parse_asignacion(self):
        identificador = self.consumir("IDENTIFICADOR")
        
        self.consumir("OP ASIGNACION")
        expresion = self.parse_expresion()
        
        self.consumir("PUNTO Y COMA")
        return AST(
            "ASIGNACION",
            valor=identificador.valor,
            hijos=[expresion]
        )

    def parse_if(self):
        self.consumir("IF")
        self.consumir("PARENTESIS IZQ")
        condicion = self.parse_expresion()
        self.consumir("PARENTESIS DER")
        bloque_if = self.parse_bloque()
        
        bloque_else = None
        if self.match("ELSE"):
            self.consumir("ELSE")
            if self.match("IF"): bloque_else = self.parse_if()
            else: bloque_else = AST("BLOQUE ELSE", hijos=self.parse_bloque())
        
        return AST(
            tipo="IF",
            hijos=[condicion, AST("BLOQUE IF", hijos=bloque_if), bloque_else]
        )
        
    def parse_bloque(self):
        self.consumir("LLAVE IZQ")
        sentencias = self.parse_sentencias()
        self.consumir("LLAVE DER")
        return sentencias
    
    def parse_llamada_funcion(self, token_name=None):
        if not token_name: token_name = self.consumir("IDENTIFICADOR")

        self.consumir("PARENTESIS IZQ")
        argumentos = self.parse_argumentos()
        self.consumir("PARENTESIS DER")
        
        return AST(tipo="LLAMADA FUNCION", valor=token_name, hijos=argumentos)
    
    def parse_argumentos(self):
        argumentos = []
        
        if self.match("PARENTESIS DER"): return argumentos
        
        while True:
            argumento = self.parse_expresion()
            if argumento: argumentos.append(argumento)
            else:
                print("Argumento inválido en llamada a función")
                return None
            
            if self.match("COMA"): self.consumir("COMA")
            else: break
            
        return argumentos
    
    def parse_while(self):
        self.consumir("WHILE")
        self.consumir("PARENTESIS IZQ")
        condicion = self.parse_condicion()
        self.consumir("PARENTESIS DER")
        
        cuerpo = self.parse_bloque()
        
        return AST(
            tipo="WHILE",
            hijos=[AST("CONDICION", hijos=[condicion]), AST("CUERPO", hijos=cuerpo)],
            valor=None
        )
    
    def parse_for(self):
        self.consumir("FOR")
        self.consumir("PARENTESIS IZQ")
        
        inicializacion = self.parse_inicializacion()
        self.consumir("PUNTO Y COMA")
        
        condicion = self.parse_expresion()
        self.consumir("PUNTO Y COMA")
        
        actualizacion = self.parse_actualizacion()
        self.consumir("PARENTESIS DER")
        
        cuerpo = self.parse_bloque()
        
        return AST(
            "FOR", 
            hijos=[
                inicializacion, condicion, actualizacion, 
                AST("CUERPO", hijos=cuerpo)
                ]
            )

    def parse_inicializacion(self):
        if self.match("TIPO DATO"):
            return self.parse_declaracion_sin_punto_y_coma()
        elif self.match("IDENTIFICADOR"):
            return self.parse_asignacion_sin_punto_y_coma()
        return None

    def parse_actualizacion(self):
        if self.match("IDENTIFICADOR"):
            if self.peek().tipo == "OP ASIGNACION":
                return self.parse_asignacion_sin_punto_y_coma()
            else:
                return self.parse_expresion()
        return None
    
    def parse_return(self):        
        self.consumir("RETURN")
        if self.match("PUNTO Y COMA"):
            self.consumir("PUNTO Y COMA")
            return AST(tipo="RETURN")
        expresion = self.parse_expresion()
        self.consumir("PUNTO_Y_COMA")
        
        return AST(
            tipo="RETURN",
            hijos=[expresion]
        )
        
    def parse_print(self):
        self.consumir("PRINT")
        self.consumir("PARENTESIS IZQ")
        expresion = self.parse_expresion()
        self.consumir("PARENTESIS DER")
        self.consumir("PUNTO Y COMA")
        return AST(tipo="PRINT", hijos=[expresion])
    
    def parse_read(self):
        self.consumir("READ")
        self.consumir("PARENTESIS IZQ")
        identificador = self.consumir("IDENTIFICADOR")
        self.consumir("PARENTESIS DER")
        self.consumir("PUNTO Y COMA")
        return AST(
            tipo="READ",
            valor=identificador.valor,
            hijos=[AST("IDENTIFICADOR", valor=identificador.valor)]
        )
    
    def parse_break(self):
        self.consumir("BREAK")
        self.consumir("PUNTO Y COMA")
        return AST("BREAK")

    def parse_continue(self):
        self.consumir("CONTINUE")
        self.consumir("PUNTO Y COMA")
        return AST("CONTINUE")
    
    def parse_asignacion_sin_punto_y_coma(self):
        identificador = self.consumir("IDENTIFICADOR")
        self.consumir("OP ASIGNACION")
        expresion = self.parse_expresion()
        return AST("ASIGNACION", valor=identificador.valor, hijos=[expresion])


    def parse_declaracion_sin_punto_y_coma(self):
        tipo_str = self.consumir("TIPO DATO").valor
        nodos_de_declaracion = []
        while True:
            identificador_token = self.consumir("IDENTIFICADOR")
            expresion_nodo = None
            if self.match("OP ASIGNACION"):
                self.consumir("OP ASIGNACION")
                expresion_nodo = self.parse_expresion()
            nodo_actual = AST("DECLARACION", valor=identificador_token.valor, hijos=[AST("TIPO", valor=tipo_str), expresion_nodo])
            nodos_de_declaracion.append(nodo_actual)
            if not self.match("COMA"):
                break
            self.consumir("COMA")
        
        return AST("LISTA_DECLARACIONES", hijos=nodos_de_declaracion)
    
    def parse_expresion(self):
        expresion = self.parse_termino_or()
        return expresion
    
    def parse_termino_or(self):
        expresion = self.parse_termino_and()
        
        while self.token_actual and self.token_actual.tipo == "OP OR":
            operador = self.consumir("OP OR")
            derecho = self.parse_termino_and()
            expresion = AST(
                tipo="EXPRESION BINARIA",
                valor=operador.tipo.lstrip("OP "),
                hijos=[expresion, derecho]
            )
        
        return expresion
    
    def parse_termino_and(self):
        expresion = self.parse_expresion_not()
        
        while self.token_actual and self.token_actual.tipo == "OP AND":
            operador = self.consumir("OP AND")
            derecho = self.parse_expresion_not()
            expresion = AST(
                tipo="EXPRESION BINARIA",
                valor=operador.tipo.lstrip("OP "),
                hijos=[expresion, derecho]
            )
        
        return expresion
    
    def parse_expresion_not(self):
        if self.match("OP NOT"):
            operador = self.consumir("OP NOT")
            expresion = self.parse_expresion_relacional()
            return AST(
                tipo="EXPRESION UNARIA",
                valor=operador.tipo.lstrip("OP "),
                hijos=[expresion]
            )
        else: return self.parse_expresion_relacional()
        
    def parse_expresion_relacional(self):
        izquierda = self.parse_expresion_aritmetica()
        
        if self.token_actual and self.token_actual.tipo in ("OP IGUAL", "OP DISTINTO", "OP MAYOR", "OP MENOR", "OP MAYOR IGUAL", "OP MENOR IGUAL"):
            operador = self.consumir(self.token_actual.tipo)
            derecha = self.parse_expresion_aritmetica()
            return AST(
                tipo="EXPRESION RELACIONAL",
                valor=operador.tipo.lstrip("OP "),
                hijos=[izquierda, derecha]
            )
        
        return izquierda
    
    def parse_expresion_aritmetica(self):
        expresion = self.parse_termino()
        
        while self.token_actual and self.token_actual.tipo in ("OP SUMA", "OP RESTA"):
            operador = self.consumir(self.token_actual.tipo)
            derecho = self.parse_termino()
            expresion = AST(
                tipo="EXPRESION BINARIA",
                valor=operador.tipo.lstrip("OP "),
                hijos=[expresion, derecho]
            )
            
        return expresion
    
    def parse_termino(self):
        termino = self.parse_factor()
        
        while self.token_actual and self.token_actual.tipo in ("OP MULTIPLICACION", "OP DIVISION"):
            operador = self.consumir(self.token_actual.tipo)
            derecho = self.parse_factor()
            
            termino = AST(
                tipo="EXPRESION BINARIA",
                valor=operador.tipo.lstrip('OP '),
                hijos=[termino, derecho]
            )
            
        return termino
    
    def parse_factor(self):
        token = self.token_actual
        
        # Número
        if self.match("ENTERO") or self.match("REAL") or self.match("CADENA") or self.match("CARACTER") or self.match("TRUE") or self.match("FALSE"):
            self.avanzar()
            return AST(tipo="LITERAL", valor=token.valor)
        
        # Identificador o llamada a función
        elif self.match("IDENTIFICADOR"):
            siguiente = self.peek()
            self.avanzar()
            
            if siguiente and siguiente.tipo == "PARENTESIS IZQ":
                return self.parse_llamada_funcion(token_name=token)
            else:
                return AST(tipo="IDENTIFICADOR", valor=token.valor)
        
        # Subexpresión (entre '()')
        elif self.match("PARENTESIS IZQ"):
            self.consumir("PARENTESIS IZQ")
            subexpresion = self.parse_expresion()
            self.consumir("PARENTESIS DER")
            return subexpresion
        
        self.avanzar()
        print(f"Factor inválido en línea {token.linea}")
        return None
        
    def parse_condicion(self): return self.parse_expresion_logica()
    
    def parse_expresion_logica(self):
        # NOT
        if self.match("OP NOT"):
            operador = self.consumir("OP NOT")
            expr = self.parse_expresion_logica()
            return AST(tipo="EXPRESION NOT", valor=operador.valor, hijos=[expr])
        
        # OR
        nodo = self.parse_expresion_and()
        while self.match("OR"):
            operador = self.consumir("OR")
            der = self.parse_expresion_and()
            nodo = AST(tipo="EXPRESION OR",valor=operador.valor,hijos=[nodo, der])
        return nodo

    def parse_expresion_and(self):
        nodo = self.parse_expresion_relacional()
        while self.match("OP AND"):
            operador = self.consumir("AND")
            derecho = self.parse_expresion_relacional()
            nodo =  AST(tipo="EXPRESION AND",valor=operador.valor,hijos=[nodo, derecho])
        return nodo

code_path = './code.txt'
tokens = Lexer(code_path).tokenize()

parser = Parser(tokens)
parser.parse()

def mostrar_ast():
    print(parser)
    
if __name__ == "__main__":
    mostrar_ast()