from dataclasses import dataclass
from typing import Optional
from src.core.exceptions import ValidacionError

@dataclass
class Categoria:
    id: Optional[int]
    nombre: str
    presupuesto_mensual: float
    color: str = "#007bff"
    icono: str = "📁"
    es_personalizada: bool = False
    
    def validar(self) -> bool:
        if not self.nombre or not self.nombre.strip():
            raise ValidacionError("El nombre de la categoría es obligatorio")
        if self.presupuesto_mensual < 0:
            raise ValidacionError("El presupuesto mensual no puede ser negativo")
        return True
    
    def __str__(self) -> str:
        return f"{self.icono} {self.nombre} (${self.presupuesto_mensual:.2f})"
    
    def __hash__(self):
        return hash((self.id, self.nombre))
    
    def __eq__(self, other):
        if not isinstance(other, Categoria):
            return False
        return self.id == other.id and self.nombre == other.nombre