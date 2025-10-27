from .variables import Variable

class ListaVariables:
    def __init__(self):
        self.variables = []

    def declarar(self, variable: Variable):
        self.variables.append(variable)

    def buscar(self, nombre):
        for variable in self.variables:
            if nombre == variable.nombre:
                return variable
        return None
    
    def __str__(self):
        if not self.variables:
            return "Tabla de Variables vacía"
        
        header = f"{'Nombre':<20} {'Tipo':<10}"
        separator = "-" * 31
        lines = ["Lista de Variables", separator, header, separator]

        for var in self.variables:
            row = f"{var.nombre:<20} {var.tipo:<10}"
            lines.append(row)
        
        return "\n".join(lines)