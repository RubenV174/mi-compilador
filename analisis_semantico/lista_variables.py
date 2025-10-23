from .variables import Variable

class ListaVariables:
    def __init__(self):
        self.variables = {}

    def declarar(self, variable: Variable):
        self.variables[variable.nombre] = variable

    def buscar(self, nombre):
        return self.variables.get(nombre)
    
    def __str__(self):
        if not self.variables:
            return "Tabla de Variables vacía"
        
        header = f"{'Nombre':<20} {'Tipo':<10}"
        separator = "-" * 31
        lines = [header, separator]

        for var in self.variables.values():
            row = f"{var.nombre:<20} {var.tipo:<10}"
            lines.append(row)
        
        return "\n".join(lines)