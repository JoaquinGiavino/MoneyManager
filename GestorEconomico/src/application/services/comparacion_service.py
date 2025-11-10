from src.domain.interfaces import IServicioGastos
from src.domain.entities import ComparacionGastos, Usuario
from src.core.exceptions import ServicioError

class ComparadorMensual:
    def comparar_meses(self, mes_actual: int, año_actual: int, 
                    mes_anterior: int, año_anterior: int,
                    servicio: IServicioGastos, usuario: Usuario) -> ComparacionGastos:
        try:
            gastos_actual = servicio.obtener_gastos_por_mes(mes_actual, año_actual, usuario)
            gastos_anterior = servicio.obtener_gastos_por_mes(mes_anterior, año_anterior, usuario)
            
            total_actual = sum(g.monto for g in gastos_actual)
            total_anterior = sum(g.monto for g in gastos_anterior)
            
            diferencia = total_actual - total_anterior
            
            if total_anterior > 0:
                porcentaje = (diferencia / total_anterior) * 100
            else:
                porcentaje = 100 if total_actual > 0 else 0
            
            return ComparacionGastos(
                diferencia_total=diferencia,
                porcentaje_cambio=porcentaje,
                mes_actual_total=total_actual,
                mes_anterior_total=total_anterior
            )
            
        except Exception as e:
            raise ServicioError(f"Error al comparar meses: {str(e)}")