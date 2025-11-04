from .cuadruplo import Cuadruplo
from analisis_sintactico.ASTNode import AST
from typing import List

class Generador_CI:
    def __init__(self):
        self.codigo = []

    def generar_lista(self):
        pass

    def visitar(self, nodo: AST):
        if nodo is None:
            raise NotImplementedError(f"Error: No existe un AST")
        
        programa: List['AST'] = nodo.hijos
        
        for sentencia in programa.hijos:
            self.visitar_sentencia(sentencia)

    def visitar_sentencia(self, nodo: AST):
        tipo_sentencia = nodo.tipo
        if tipo_sentencia == 'DECLARACION': 
            tipo_sentencia = 'ASIGNACION'

        nombre_metodo = 'visitar_' + tipo_sentencia.replace(' ', '_')

        metodo_visita = getattr(Generador_CI, nombre_metodo)

        metodo_visita(nodo)

    def visitar_ASIGNACION(self, nodo: AST):
        if nodo.hijos[1] is None:
            return
        elif nodo.hijos[1].valor == 'EXPRESION BINARIA':
            op1 = self.nueva_temp(nodo.hijos[1].hijos)
        # elif nodo.hijos[1].valor == 'EXPRESION UNARIA':
        else:
            op1 = nodo.hijos[1].valor

        return Cuadruplo('=', op1, None, nodo.valor)

    def add_code(self, operador: str, op1: str, op2: str = None, res: str = None):
        self.codigo.append(Cuadruplo(operador, op1, op2, res))