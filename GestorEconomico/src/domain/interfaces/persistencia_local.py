from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from src.domain.entities import Gasto, Categoria, Usuario

class IPersistenciaLocal(ABC):
    @abstractmethod
    def guardar_gasto(self, gasto: Gasto) -> None:
        pass
    
    @abstractmethod
    def obtener_gastos(self, fecha_inicio: date, fecha_fin: date, usuario: Usuario) -> List[Gasto]:
        pass
    
    @abstractmethod
    def obtener_categorias(self) -> List[Categoria]:
        pass
    
    @abstractmethod
    def guardar_categoria(self, categoria: Categoria) -> None:
        pass
    
    @abstractmethod
    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        pass
    
    # AGREGAR ESTE MÉTODO NUEVO:
    @abstractmethod
    def eliminar_gasto(self, gasto_id: int, usuario: Usuario) -> bool:
        pass