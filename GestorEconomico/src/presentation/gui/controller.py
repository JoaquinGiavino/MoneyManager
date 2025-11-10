from datetime import date
from src.domain.entities import Usuario, TipoAlerta
from src.application.services import ServicioGastos, AnalizadorGastos, GestorReportes, ComparadorMensual, ServicioCategorias
from src.application.strategies import AnalisisTotal, AnalisisPorCategoria, AnalisisTendencias
from src.application.exporters import GestorExportacion
from src.infrastructure.persistence import PersistenciaSQLite
from src.infrastructure.notifications import GestorNotificaciones
from src.application.factories import GastoFactory

class ControllerGastos:
    """Controlador principal del Gestor Económico"""
    
    def __init__(self):
        # Inicializar infraestructura
        self.persistence = PersistenciaSQLite()
        self.notificador = GestorNotificaciones()
        
        # Inicializar servicios
        self.servicio_gastos = ServicioGastos(self.persistence)
        
        # Estrategias de análisis
        estrategias = [
            AnalisisTotal(),
            AnalisisPorCategoria(),
            AnalisisTendencias()
        ]
        
        self.analizador = AnalizadorGastos(estrategias)
        self.gestor_reportes = GestorReportes(self.servicio_gastos)
        self.gestor_exportacion = GestorExportacion()
        self.comparador = ComparadorMensual()
        self.servicio_categorias = ServicioCategorias(self.persistence)
        
        # Usuario actual del Gestor Económico
        self.usuario_actual = Usuario(
            id=1, 
            nombre="Usuario Gestor Económico", 
            email="usuario@gestoreconomico.com"
        )
        
        # Vistas (se establecerán después)
        self.vista_principal = None
        
        print("✅ Controlador del Gestor Económico inicializado")
    
    def agregar_gasto(self, descripcion: str, monto: float, fecha: date, categoria):
        """Agregar un nuevo gasto al Gestor Económico"""
        try:
            gasto = GastoFactory.crear_gasto(
                descripcion=descripcion,
                monto=monto,
                fecha=fecha,
                categoria=categoria,
                usuario=self.usuario_actual
            )
            
            self.servicio_gastos.registrar_gasto(gasto)
            
            # Enviar notificación
            self.notificador.enviar_alerta(
                TipoAlerta.NUEVO_GASTO,
                f"💸 Nuevo gasto registrado: {descripcion} - ${monto:.2f}",
                self.usuario_actual
            )
            
            self.actualizar_vistas()
            return True
            
        except Exception as e:
            print(f"❌ Error al agregar gasto: {e}")
            return False
    
    def eliminar_gasto(self, gasto_id: int) -> bool:
        """Eliminar un gasto del Gestor Económico"""
        try:
            resultado = self.servicio_gastos.eliminar_gasto(gasto_id, self.usuario_actual)
            
            if resultado:
                # Enviar notificación
                self.notificador.enviar_alerta(
                    TipoAlerta.NUEVO_GASTO,  # Podríamos crear TipoAlerta.GASTO_ELIMINADO
                    f"🗑️ Gasto eliminado correctamente (ID: {gasto_id})",
                    self.usuario_actual
                )
                
                self.actualizar_vistas()
            
            return resultado
            
        except Exception as e:
            print(f"❌ Error al eliminar gasto: {e}")
            return False
    
    def obtener_gastos_mes_actual(self):
        """Obtener gastos del mes actual del Gestor Económico"""
        hoy = date.today()
        return self.servicio_gastos.obtener_gastos_por_mes(hoy.month, hoy.year, self.usuario_actual)
    
    def obtener_gastos_por_mes(self, mes: int, año: int):
        """Obtener gastos de un mes específico"""
        return self.servicio_gastos.obtener_gastos_por_mes(mes, año, self.usuario_actual)
    
    def obtener_categorias(self):
        """Obtener todas las categorías del Gestor Económico"""
        return self.servicio_categorias.obtener_todas()
    
    def generar_reporte_mensual(self, mes: int, año: int):
        """Generar reporte mensual del Gestor Económico"""
        return self.gestor_reportes.generar_reporte_mensual(mes, año, self.usuario_actual)
    
    def comparar_meses(self, mes_actual: int, año_actual: int, 
                    mes_anterior: int, año_anterior: int):
        """Comparar gastos entre dos meses en el Gestor Económico"""
        return self.comparador.comparar_meses(
            mes_actual, año_actual, mes_anterior, año_anterior,
            self.servicio_gastos, self.usuario_actual
        )
    
    def exportar_datos(self, formato: str):
        """Exportar datos del Gestor Económico"""
        gastos = self.obtener_gastos_mes_actual()
        return self.gestor_exportacion.exportar(gastos, formato)
    
    def actualizar_vistas(self):
        """Actualizar todas las vistas del Gestor Económico"""
        if self.vista_principal:
            gastos = self.obtener_gastos_mes_actual()
            self.vista_principal.mostrar_gastos(gastos)
            
            alertas = self.analizador.verificar_alertas(gastos)
            if TipoAlerta.PRESUPUESTO_EXCEDIDO in alertas:
                self.notificador.enviar_alerta(
                    TipoAlerta.PRESUPUESTO_EXCEDIDO,
                    "¡Alerta! Has excedido el presupuesto en alguna categoría",
                    self.usuario_actual
                )