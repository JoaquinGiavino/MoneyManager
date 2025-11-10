from typing import List
from src.domain.entities import Gasto
from src.domain.interfaces import Exportable

class ExportadorCSV(Exportable):
    def exportar(self, gastos: List[Gasto]) -> str:
        if not gastos:
            return ""
        
        output = []
        output.append("Fecha,Descripcion,Monto,Categoria,Moneda,Presupuesto_Categoria")
        
        for gasto in gastos:
            output.append(
                f"{gasto.fecha},"
                f"'{gasto.descripcion}',"
                f"{gasto.monto},"
                f"{gasto.categoria.nombre},"
                f"{gasto.moneda.value},"
                f"{gasto.categoria.presupuesto_mensual}"
            )
        
        return "\n".join(output)