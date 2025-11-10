from datetime import date, timedelta
from typing import Dict
from src.domain.interfaces import IServicioGastos
from src.domain.entities import ReporteGastos, Usuario
from src.core.exceptions import ServicioError

class GestorReportes:
    def __init__(self, servicio: IServicioGastos):
        self.servicio = servicio
    
    def generar_reporte_mensual(self, mes: int, año: int, usuario: Usuario) -> ReporteGastos:
        try:
            gastos = self.servicio.obtener_gastos_por_mes(mes, año, usuario)
            
            fecha_inicio = date(año, mes, 1)
            if mes == 12:
                fecha_fin = date(año + 1, 1, 1) - timedelta(days=1)
            else:
                fecha_fin = date(año, mes + 1, 1) - timedelta(days=1)
            
            por_categoria = {}
            total = 0.0
            
            for gasto in gastos:
                total += gasto.monto
                categoria = gasto.categoria
                
                if categoria not in por_categoria:
                    por_categoria[categoria] = 0.0
                por_categoria[categoria] += gasto.monto
            
            return ReporteGastos(
                total=total,
                por_categoria=por_categoria,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            
        except Exception as e:
            raise ServicioError(f"Error al generar reporte: {str(e)}")
    
    def generar_reporte_anual(self, año: int, usuario: Usuario) -> Dict[int, ReporteGastos]:
        reportes = {}
        
        for mes in range(1, 13):
            try:
                reporte = self.generar_reporte_mensual(mes, año, usuario)
                reportes[mes] = reporte
            except ServicioError:
                continue
        
        return reportes