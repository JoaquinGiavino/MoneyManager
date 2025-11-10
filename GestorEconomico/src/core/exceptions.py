class GestionGastosError(Exception):
    """Excepción base para la aplicación"""
    pass

class ValidacionError(GestionGastosError):
    """Error de validación de datos"""
    pass

class PersistenciaError(GestionGastosError):
    """Error de persistencia de datos"""
    pass

class ServicioError(GestionGastosError):
    """Error en servicios de aplicación"""
    pass