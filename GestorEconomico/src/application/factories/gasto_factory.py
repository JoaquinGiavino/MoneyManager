from datetime import date
from src.domain.entities import Gasto, Moneda

class GastoFactory:
    @staticmethod
    def crear_gasto(descripcion: str, monto: float, fecha: date, 
                   categoria, usuario, moneda: Moneda = Moneda.ARS):
        return Gasto(
            id=None,
            descripcion=descripcion,
            monto=monto,
            fecha=fecha,
            categoria=categoria,
            usuario=usuario,
            moneda=moneda
        )