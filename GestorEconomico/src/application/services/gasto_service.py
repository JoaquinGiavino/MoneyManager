from datetime import date, timedelta
from typing import List
from src.domain.interfaces import IServicioGastos, IPersistenciaLocal
from src.domain.entities import Gasto, Usuario, Categoria
from src.core.exceptions import ServicioError, ValidacionError

class ServicioGastos(IServicioGastos):
    """Servicio principal para gestión de gastos del Gestor Económico"""
    
    def __init__(self, persistencia: IPersistenciaLocal):
        self.persistencia = persistencia
        print("✅ Servicio de Gastos del Gestor Económico inicializado")
    
    def registrar_gasto(self, gasto: Gasto) -> None:
        """Registrar un nuevo gasto en el Gestor Económico"""
        try:
            if not gasto.validar():
                raise ValidacionError("El gasto no pasa la validación del Gestor Económico")
            
            self.persistencia.guardar_gasto(gasto)
            print(f"✅ Gasto registrado exitosamente: {gasto.descripcion}")
            
        except Exception as e:
            raise ServicioError(f"Error al registrar gasto en el Gestor Económico: {str(e)}")
    
    def obtener_gastos_por_mes(self, mes: int, año: int, usuario: Usuario) -> List[Gasto]:
        """Obtener gastos de un mes específico del Gestor Económico"""
        try:
            fecha_inicio = date(año, mes, 1)
            if mes == 12:
                fecha_fin = date(año + 1, 1, 1) - timedelta(days=1)
            else:
                fecha_fin = date(año, mes + 1, 1) - timedelta(days=1)
            
            gastos = self.persistencia.obtener_gastos(fecha_inicio, fecha_fin, usuario)
            print(f"✅ Obtenidos {len(gastos)} gastos para {mes}/{año}")
            return gastos
            
        except Exception as e:
            raise ServicioError(f"Error al obtener gastos del mes en el Gestor Económico: {str(e)}")
    
    def obtener_gastos_por_categoria(self, categoria: Categoria, usuario: Usuario) -> List[Gasto]:
        """Obtener gastos por categoría en el Gestor Económico"""
        try:
            # Obtener todos los gastos y filtrar por categoría
            todos_gastos = self.persistencia.obtener_gastos(
                date(2000, 1, 1),  # Fecha muy antigua
                date.today(),
                usuario
            )
            
            gastos_filtrados = [gasto for gasto in todos_gastos if gasto.categoria.id == categoria.id]
            print(f"✅ Obtenidos {len(gastos_filtrados)} gastos para categoría {categoria.nombre}")
            return gastos_filtrados
            
        except Exception as e:
            raise ServicioError(f"Error al obtener gastos por categoría: {str(e)}")
    
    def obtener_gastos_por_rango_fechas(self, fecha_inicio: date, fecha_fin: date, usuario: Usuario) -> List[Gasto]:
        """Obtener gastos dentro de un rango de fechas específico"""
        try:
            gastos = self.persistencia.obtener_gastos(fecha_inicio, fecha_fin, usuario)
            print(f"✅ Obtenidos {len(gastos)} gastos del {fecha_inicio} al {fecha_fin}")
            return gastos
        except Exception as e:
            raise ServicioError(f"Error al obtener gastos por rango de fechas: {str(e)}")
    
    def eliminar_gasto(self, gasto_id: int, usuario: Usuario) -> bool:
        """Eliminar un gasto del Gestor Económico"""
        try:
            if gasto_id <= 0:
                raise ValidacionError("ID de gasto inválido")
            
            resultado = self.persistencia.eliminar_gasto(gasto_id, usuario)
            
            if resultado:
                print(f"✅ Gasto {gasto_id} eliminado del servicio")
            else:
                print(f"⚠️ No se pudo eliminar el gasto {gasto_id}")
                
            return resultado
            
        except Exception as e:
            raise ServicioError(f"Error al eliminar gasto: {str(e)}")