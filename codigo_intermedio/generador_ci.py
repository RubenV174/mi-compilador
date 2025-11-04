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
    }

    def __init__(self):
        self.codigo = []
        self.c_temp = 0
    
    def __str__(self):
        code = "\nCodigo Intermedio\n"
        for c in self.codigo:
            if c.op == '=': code += f"{c.res} {c.op} {c.op1}\n"
            else: code += f"{c.res} = {c.op1} {c.op} {c.op2}\n"

        return code

    def generar_lista(self, nodo: AST):
        self.visitar(nodo)

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

    def visitar_DECLARACION(self, nodo: AST):
        if not nodo.hijos[0]:
            return
        elif nodo.hijos[1] and nodo.hijos[1].tipo == 'EXPRESION BINARIA':
            op1 = self.visitar_EXPRESION_BINARIA(nodo.hijos[1])
        # elif nodo.hijos[1].valor == 'EXPRESION UNARIA':
        else:
            if not nodo.hijos[1]: return
            op1 = nodo.hijos[1].valor

        self.add_code('=', op1, None, nodo.valor)
    
    def visitar_ASIGNACION(self, nodo: AST):
        if not nodo.hijos[0]:
            return
        elif nodo.hijos[0] and nodo.hijos[0].tipo == 'EXPRESION BINARIA':
            op1 = self.visitar_EXPRESION_BINARIA(nodo.hijos[0])
        # elif nodo.hijos[1].valor == 'EXPRESION UNARIA':
        else:
            op1 = nodo.hijos[0].valor
        self.add_code('=', op1, None, nodo.valor)

    def visitar_EXPRESION_BINARIA(self, nodo: AST):
        tipo = nodo.tipo
        operador = nodo.valor
        operador = self.OPERADORES.get(operador)
        hijos = nodo.hijos
        op = []
        for hijo in hijos:
            if hijo.tipo == 'EXPRESION BINARIA':
                operando = self.visitar_EXPRESION_BINARIA(hijo)
                op.append(operando)
            elif hijo.tipo == 'LITERAL':
                op.append(hijo.valor)
        resultado = self.nueva_temp()
        self.add_code(operador, op[0], op[1], resultado)
        return resultado

    def nueva_temp(self):
        self.c_temp += 1
        return f"t{self.c_temp}"

    def add_code(self, operador: str, op1: str, op2: str = None, res: str = None):
        self.codigo.append(Cuadruplo(operador, op1, op2, res))