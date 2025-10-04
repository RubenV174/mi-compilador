from dataclasses import dataclass, field
from typing import List, Optional, Union

@dataclass
class AST:
    tipo: str
    valor: Optional[Union[str, int]] = None
    hijos: List['AST'] = field(default_factory=list)