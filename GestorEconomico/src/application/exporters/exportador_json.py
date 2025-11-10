import json
from typing import List
from src.domain.entities import Gasto
from src.domain.interfaces import Exportable

class ExportadorJSON(Exportable):
    def exportar(self, gastos: List[Gasto]) -> str:
        datos = []
        
        for gasto in gastos:
            datos.append({
                "fecha": gasto.fecha.isoformat(),
                "descripcion": gasto.descripcion,
                "monto": gasto.monto,
                "categoria": {
                    "nombre": gasto.categoria.nombre,
                    "presupuesto_mensual": gasto.categoria.presupuesto_mensual,
                    "color": gasto.categoria.color,
                    "icono": gasto.categoria.icono
                },
                "moneda": gasto.moneda.value,
                "usuario": gasto.usuario.nombre
            })
        
        return json.dumps({
            "gastos": datos,
            "total_registros": len(gastos),
            "fecha_exportacion": "datetime"
        }, indent=2, ensure_ascii=False)