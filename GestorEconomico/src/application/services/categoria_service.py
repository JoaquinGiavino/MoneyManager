from typing import List
from src.domain.interfaces import IPersistenciaLocal
from src.domain.entities import Categoria
from src.core.exceptions import ServicioError

class ServicioCategorias:
    def __init__(self, persistencia: IPersistenciaLocal):
        self.persistencia = persistencia
    
    def obtener_todas(self) -> List[Categoria]:
        try:
            return self.persistencia.obtener_categorias()
        except Exception as e:
            raise ServicioError(f"Error al obtener categorías: {str(e)}")
    
    def guardar(self, categoria: Categoria) -> None:
        try:
            if not categoria.validar():
                raise ValueError("Categoría no válida")
            
            self.persistencia.guardar_categoria(categoria)
        except Exception as e:
            raise ServicioError(f"Error al guardar categoría: {str(e)}")
    
    def obtener_por_nombre(self, nombre: str) -> Categoria:
        categorias = self.obtener_todas()
        for categoria in categorias:
            if categoria.nombre == nombre:
                return categoria
        raise ServicioError(f"Categoría '{nombre}' no encontrada")