from dataclasses import dataclass
from typing import Optional
from src.core.exceptions import ValidacionError

@dataclass
class Usuario:
    id: Optional[int]
    nombre: str
    email: str
    
    def validar(self) -> bool:
        if not self.nombre or not self.nombre.strip():
            raise ValidacionError("El nombre del usuario es obligatorio")
        if not self.email or '@' not in self.email:
            raise ValidacionError("El email del usuario no es válido")
        return True