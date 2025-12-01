from analisis_semantico.lista_variables import ListaVariables
from analisis_semantico.variables import Variable
from analisis_sintactico.ASTNode import AST

class Semantic:
    def __init__(self):
        self.variables = ListaVariables()
    
    def verificar_declaracion(self, nombre: str, tipo: str):
        if self.variables.buscar(nombre) is not None:
            raise NameError(f"Error Semántico: La variable '{nombre}' ya ha sido declarada.")
            
        variable = Variable(nombre, tipo)
        self.variables.declarar(variable)
        
    def verificar_uso_variable(self, nombre: str):
        if self.variables.buscar(nombre) is None:
            raise NameError(f"Error Semántico: La variable '{nombre}' no ha sido declarada.")
            
    # Algoritmo 3: Incompatibilidad de tipos (en asignación)
    def verificar_asignacion(self, nodo: AST):
        nombre = nodo.valor
        
        variable = self.variables.buscar(nombre)
        if variable is None:
            raise NameError(f"Error Semántico: La variable '{nombre}' no ha sido declarada.")
        
        tipo_esperado = variable.tipo

        if not nodo.hijos or not isinstance(nodo.hijos, list):
            raise ValueError("Nodo de asignación malformado: falta la expresión")
        nodo_expresion = nodo.hijos[0]
        tipo_expresion = self.evaluar_tipo_expresion(nodo_expresion)
        
        es_compatible = (tipo_esperado == tipo_expresion) or (tipo_esperado == "double" and tipo_expresion == "int")
            
        if not es_compatible:
            raise TypeError(f"Error de Tipos: No se puede asignar tipo '{tipo_expresion}' a la variable '{nombre}' de tipo '{tipo_esperado}'.")            
        
    def evaluar_tipo_expresion(self, nodo: AST):
        if not nodo:
            return 'void'
        
        tipo = nodo.tipo
        
        if tipo == 'LITERAL':
            valor = nodo.valor
            if valor in ['true', 'false']: return 'boolean'
            if isinstance(valor, str):
                if valor.startswith('"'): return 'string'
                if valor.startswith("'"): return 'char'
            if '.' in str(valor): return 'double'
            return 'int'
        
        if tipo == "IDENTIFICADOR":
            nombre = nodo.valor
            variable = self.variables.buscar(nombre)
            if not variable:
                raise NameError(f"Error Semántico: La variable '{nombre}' no ha sido declarada.")
            return variable.tipo
        
        if tipo == 'EXPRESION BINARIA' or tipo == 'EXPRESION RELACIONAL':
            l_tipo = self.evaluar_tipo_expresion(nodo.hijos[0])
            r_tipo = self.evaluar_tipo_expresion(nodo.hijos[1])
            op = nodo.valor
            
            if op in ['IGUAL', 'DISTINTO', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL']:
                if l_tipo in ['int', 'double'] and r_tipo in ['int', 'double']:
                    return 'boolean'
                if op in ['IGUAL', 'DISTINTO']:
                    return 'boolean'
                else:
                    raise TypeError(f"Error de Tipos: No se pueden comparar '{l_tipo}' y '{r_tipo}'.")
            
            if op in ['AND', 'OR']:
                if l_tipo == 'boolean' and r_tipo == 'boolean':
                    return 'boolean'
                else:
                    raise TypeError(f"Error de Tipos: Operador lógico inválido entre '{l_tipo}' y '{r_tipo}'.")
            
            if op in ['SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION']:
                if (l_tipo == 'int' and r_tipo == 'int') and op in ['SUMA', 'RESTA', 'MULTIPLICACION']:
                    return 'int'
                if l_tipo in ['int', 'double'] and r_tipo in ['int', 'double']:
                    return 'double'
                if l_tipo in ['string', 'char', 'int', 'double'] and r_tipo in ['string', 'char', 'int', 'double']:
                    return 'string'
                else:
                    raise TypeError(f"Error de Tipos: Operación aritmética inválida entre '{l_tipo}' y '{r_tipo}'.")
        
        if tipo == "EXPRESION UNARIA":
            tipo_expr = self.evaluar_tipo_expresion(nodo.hijos[0])
            op = nodo.valor
            if op == 'NOT' and tipo_expr == 'boolean':
                return 'boolean'
            raise TypeError(f"Error de Tipos: El operador unario '{op}' no se puede aplicar a '{tipo_expr}'.")
            
        raise TypeError(f"No se pudo determinar el tipo del nodo: '{tipo}'")
