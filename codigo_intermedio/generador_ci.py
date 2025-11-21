from .cuadruplo import Cuadruplo
from analisis_sintactico.ASTNode import AST
from typing import List

class Generador_CI:
    OPERADORES = {
        'SUMA': '+',
        'RESTA': '-',
        'MULTIPLICACION': '*',
        'DIVISION': '/',
        'MENOR': '<',
        'MENOR IGUAL': '<=',
        'MAYOR': '>',
        'MAYOR IGUAL': '>=',
        'AND': '&&',
        'OR': '||',
        'NOT': '!',
        'IGUAL': '==',
        'DISTINTO': '!=',
    }

    def __init__(self):
        self.codigo = []
        self.c_temp = 0
        self.c_brincoA = 0
        self.c_brincoB = 0
        self.c_brincoC = 0
        self.c_brincoD = 0
        self.brinco_break = None
        self.brinco_continue = None
    
    def __str__(self):
        code = "\nCodigo Intermedio\n"
        formato_tabla = ('+' + '-' * 11) * 4 + '+ \n'
        code += formato_tabla * 2 
        code += f"|{'OP':>10} |{'OP1':>10} |{'OP2':>10} |{'RES':>10} |\n"
        code += formato_tabla
        for c in self.codigo:
            code += f'|{c.op:>10} '
            if c.op1: code += f'|{c.op1:>10} '
            else: code += '|           '
            if c.op2: code += f'|{c.op2:>10} '
            else: code += '|           '
            if c.res: code += f'|{c.res:>10} '
            else: code += '|           '
            code += '|\n'
            code += formato_tabla
        return code
    
    def nueva_temp(self) -> str:
        self.c_temp += 1
        return f"t{self.c_temp}"
    
    def nuevo_brinco(self, tipo: str) -> str:
        if tipo == 'A':
            self.c_brincoA += 1
            return f"{tipo}{self.c_brincoA}"
        elif tipo == 'B':
            self.c_brincoB += 1
            return f"{tipo}{self.c_brincoB}"
        elif tipo == 'C':
            self.c_brincoC += 1
            return f"{tipo}{self.c_brincoC}"
        elif tipo == 'D':
            self.c_brincoD += 1
            return f"{tipo}{self.c_brincoD}"

    def add_code(self, operador: str, op1: str = None, op2: str = None, res: str = None):
        self.codigo.append(Cuadruplo(operador, op1, op2, res))

    def generar_lista(self, nodo: AST):
        self.visitar(nodo)
        return self.codigo

    def visitar(self, nodo: AST):
        if nodo is None:
            raise NotImplementedError(f"Error: No existe un AST")
        
        programa: List['AST'] = nodo.hijos[0].hijos
        
        for sentencia in programa:
            self.visitar_sentencia(sentencia)

    def visitar_sentencia(self, nodo: AST):
        tipo_sentencia = nodo.tipo
        
        nombre_metodo = 'visitar_' + tipo_sentencia.replace(' ', '_')

        metodo_visita = getattr(Generador_CI, nombre_metodo)

        metodo_visita(self, nodo)

    def visitar_expresion(self, nodo: AST):
        tipo = nodo.tipo
        if tipo == 'EXPRESION UNARIA': return self.visitar_EXPRESION_UNARIA(nodo)
        elif tipo == 'EXPRESION BINARIA': return self.visitar_EXPRESION_BINARIA(nodo)
        else: return

    def visitar_DECLARACION(self, nodo: AST):
        if not nodo.hijos[0] or not nodo.hijos[1]:
            return
        elif nodo.hijos[1].tipo in ['LITERAL', 'IDENTIFICADOR']:
            op1 = nodo.hijos[1].valor
        else:
            op1 = self.visitar_expresion(nodo.hijos[1])

        self.add_code(operador='=', op1=op1, res=nodo.valor)
    
    def visitar_ASIGNACION(self, nodo: AST):
        if not nodo.hijos[0]:
            return
        elif nodo.hijos[0].tipo in ['LITERAL', 'IDENTIFICADOR']:
            op1 = nodo.hijos[0].valor
        else:
            op1 = self.visitar_expresion(nodo.hijos[0])
        self.add_code(operador='=', op1=op1, res=nodo.valor)

    def visitar_EXPRESION_BINARIA(self, nodo: AST):
        operador = self.OPERADORES.get(nodo.valor)
        hijos = nodo.hijos
        op = []
        for hijo in hijos:

            if hijo.tipo == 'LITERAL':
                op.append(hijo.valor)
            elif hijo.tipo == 'IDENTIFICADOR':
                op.append(hijo.valor)
            else:
                operando = self.visitar_expresion(hijo)
                op.append(operando)

        resultado = self.nueva_temp()
        self.add_code(operador, op[0], op[1], resultado)
        return resultado
    
    def visitar_EXPRESION_UNARIA(self, nodo: AST):
        operador = self.OPERADORES.get(nodo.valor)
        hijo = nodo.hijos[0]
        operando: str

        if hijo.tipo in ['LITERAL', 'IDENTIFICADOR']:
            operando = hijo.valor
        else:
            operando = self.visitar_expresion(hijo)

        resultado = self.nueva_temp()
        self.add_code(operador=operador, op1=operando, res=resultado)
        return resultado
    
    def visitar_IF(self, nodo: AST):
        condicion = nodo.hijos[0]
        if condicion.hijos[0].tipo in ['TRUE', 'FALSE']:
            self.visitar_TRUE_FALSE(condicion)
        else:
            self.visitar_expresion(condicion)
        
        brf = self.nuevo_brinco('A')
        self.add_code(operador="BRF", res=brf)
        
        sentencias1 = nodo.hijos[1].hijos
        for sentencia in sentencias1:
            self.visitar_sentencia(sentencia)
        
        bri = self.nuevo_brinco('B')
        self.add_code(operador="BRI", res=bri)
        
        if not nodo.hijos[2]: return
        sentencias2 = nodo.hijos[2].hijos
        for sentencia in sentencias2:
            self.visitar_sentencia(sentencia)

    def visitar_WHILE(self, nodo: AST):
        condicion = nodo.hijos[0]
        if condicion.hijos[0].tipo in ['TRUE', 'FALSE']:
            self.visitar_TRUE_FALSE(condicion)
        else:
            self.visitar_expresion(condicion)

        brf = self.nuevo_brinco('C')
        self.add_code(operador="BRF", res=brf)

        sentencias = nodo.hijos[1].hijos
        for sentencia in sentencias:
            self.visitar_sentencia(sentencia)

        bri = self.nuevo_brinco('D')
        self.add_code(operador="BRI", res=bri)

    def visitar_FOR(self, nodo: AST):
        if nodo.hijos[0].tipo == 'DECLARACION':
            inicializacion = nodo.hijos[0].hijos
            self.visitar_DECLARACION(inicializacion)
        elif nodo.hijos[0].tipo == 'ASIGNACION':
            inicializacion = nodo.hijos[0].hijos
            self.visitar_ASIGNACION(inicializacion)

        condicion = nodo.hijos[1]
        if condicion.hijos[0].tipo in ['TRUE', 'FALSE']:
            self.visitar_TRUE_FALSE(condicion)
        else:
            self.visitar_expresion(condicion)

        brf = self.nuevo_brinco('C')
        self.add_code(operador="BRF", res=brf)

        cuerpo = nodo.hijos[3].hijos
        for sentencia in cuerpo:
            self.visitar_sentencia(sentencia)

        actualizacion = nodo.hijos[2]
        self.visitar_ASIGNACION(actualizacion)

        bri = self.nuevo_brinco('D')
        self.add_code(operador="BRI", res=bri)

    def visitar_TRUE_FALSE(self, nodo: AST):
        valor = nodo.hijos[0].valor
        self.add_code(operador='=', op1=valor, res=self.nueva_temp())

    def visitar_PRINT(self, nodo: AST):
        if not nodo.hijos[0]:
            return
        
        elif nodo.hijos[0].tipo in ['LITERAL', 'IDENTIFICADOR']:
            op1 = nodo.hijos[0].valor
        else:
            op1 = self.visitar_expresion(nodo.hijos[0])
        self.add_code(operador='print', op1=op1, res=nodo.valor)

    def visitar_RETURN(self, nodo: AST):
        if nodo.hijos:
            op1 = self.visitar_expresion(nodo.hijos[0])
            self.add_code('return', op1)
        else: self.add_code('return')

    def visitar_BREAK(self, nodo: AST):
        self.add_code('break')
    
    def visitar_CONTINUE(self, nodo: AST):
        self.add_code('continue')