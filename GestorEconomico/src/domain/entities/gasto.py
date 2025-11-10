from dataclasses import dataclass
from datetime import date
from typing import Optional
from src.core.exceptions import ValidacionError
from .categoria import Categoria
from .usuario import Usuario
from .moneda import Moneda

@dataclass
class Gasto:
    id: Optional[int]
    descripcion: str
    monto: float
    fecha: date
    categoria: Categoria
    usuario: Usuario
    moneda: Moneda = Moneda.ARS
    
    def validar(self) -> bool:
        if not self.descripcion or not self.descripcion.strip():
            raise ValidacionError("La descripción del gasto es obligatoria")
        if self.monto <= 0:
            raise ValidacionError("El monto del gasto debe ser mayor a 0")
        if self.fecha > date.today():
            raise ValidacionError("La fecha del gasto no puede ser futura")
        
        self.categoria.validar()
        self.usuario.validar()
        
        return True