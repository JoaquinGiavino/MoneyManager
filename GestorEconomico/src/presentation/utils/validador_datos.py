from datetime import date
from src.core.exceptions import ValidacionError

class ValidadorDatos:
    @staticmethod
    def validar_monto(monto: float) -> bool:
        if monto <= 0:
            raise ValidacionError("El monto debe ser mayor a 0")
        return True
    
    @staticmethod
    def validar_fecha(fecha: date) -> bool:
        if fecha > date.today():
            raise ValidacionError("La fecha no puede ser futura")
        return True
    
    @staticmethod
    def validar_descripcion(descripcion: str) -> bool:
        if not descripcion or not descripcion.strip():
            raise ValidacionError("La descripción es obligatoria")
        if len(descripcion) > 200:
            raise ValidacionError("La descripción es demasiado larga")
        return True