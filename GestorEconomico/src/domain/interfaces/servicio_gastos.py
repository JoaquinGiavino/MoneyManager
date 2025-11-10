from abc import ABC, abstractmethod
from typing import List
from src.domain.entities import Gasto, Usuario, Categoria

class IServicioGastos(ABC):
    @abstractmethod
    def registrar_gasto(self, gasto: Gasto) -> None:
        pass
    
    @abstractmethod
    def obtener_gastos_por_mes(self, mes: int, año: int, usuario: Usuario) -> List[Gasto]:
        pass
    
    @abstractmethod
    def obtener_gastos_por_categoria(self, categoria: Categoria, usuario: Usuario) -> List[Gasto]:
        pass