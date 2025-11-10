from datetime import date
from src.domain.entities import Moneda
from src.core.exceptions import ValidacionError

class FormatoRegional:
    @staticmethod
    def formatear_fecha(fecha: date) -> str:
        return fecha.strftime("%d/%m/%Y")
    
    @staticmethod
    def formatear_moneda(monto: float, moneda: Moneda) -> str:
        simbolos = {
            Moneda.ARS: "$",
            Moneda.USD: "US$",
            Moneda.EUR: "€"
        }
        
        simbolo = simbolos.get(moneda, "$")
        return f"{simbolo}{monto:,.2f}"
    
    @staticmethod
    def parsear_fecha(fecha_str: str) -> date:
        try:
            return date.fromisoformat(fecha_str)
        except ValueError:
            try:
                day, month, year = map(int, fecha_str.split('/'))
                return date(year, month, day)
            except ValueError:
                raise ValidacionError("Formato de fecha inválido. Use DD/MM/YYYY")