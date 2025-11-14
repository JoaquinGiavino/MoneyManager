import json
from typing import List
from datetime import datetime
from src.domain.entities import Gasto
from src.domain.interfaces import Exportable

class ExportadorJSON(Exportable):
    def exportar(self, gastos: List[Gasto]) -> str:
        datos = {
            "exportacion": {
                "fecha": datetime.now().isoformat(),
                "total_gastos": len(gastos),
                "version": "1.0"
            },
            "gastos": []
        }
        
        for gasto in gastos:
            gasto_data = {
                "fecha": gasto.fecha.isoformat(),
                "descripcion": gasto.descripcion,
                "monto": gasto.monto,
                "categoria": gasto.categoria.nombre,
                "moneda": gasto.moneda.value
            }
            datos["gastos"].append(gasto_data)
        
        return json.dumps(datos, indent=2, ensure_ascii=False)