from dataclasses import dataclass

@dataclass
class Token:
    id: int
    tipo: str
    valor: str
    linea: int
    pos: int