from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Cuadruplo:
    op: str
    op1: Optional[str] = None
    op2: Optional[str] = None
    res: Optional[str] = None