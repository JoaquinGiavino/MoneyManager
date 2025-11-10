import xml.etree.ElementTree as ET
from typing import List
from src.domain.entities import Gasto
from src.domain.interfaces import Exportable

class ExportadorXML(Exportable):
    def exportar(self, gastos: List[Gasto]) -> str:
        root = ET.Element("gastos")
        root.set("total", str(len(gastos)))
        
        for gasto in gastos:
            gasto_elem = ET.SubElement(root, "gasto")
            
            ET.SubElement(gasto_elem, "fecha").text = gasto.fecha.isoformat()
            ET.SubElement(gasto_elem, "descripcion").text = gasto.descripcion
            ET.SubElement(gasto_elem, "monto").text = str(gasto.monto)
            ET.SubElement(gasto_elem, "moneda").text = gasto.moneda.value
            
            categoria_elem = ET.SubElement(gasto_elem, "categoria")
            categoria_elem.set("nombre", gasto.categoria.nombre)
            categoria_elem.set("presupuesto", str(gasto.categoria.presupuesto_mensual))
            categoria_elem.set("color", gasto.categoria.color)
            categoria_elem.set("icono", gasto.categoria.icono)
            
            usuario_elem = ET.SubElement(gasto_elem, "usuario")
            usuario_elem.set("nombre", gasto.usuario.nombre)
            usuario_elem.set("email", gasto.usuario.email)
        
        return ET.tostring(root, encoding="unicode", method="xml")