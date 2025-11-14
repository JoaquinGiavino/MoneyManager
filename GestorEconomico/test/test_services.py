import unittest
from datetime import date, timedelta
from unittest.mock import Mock, MagicMock
import sys
import os

# Agregar el directorio src al path para las importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.domain.entities import Usuario, Categoria, Gasto, Moneda
from src.application.services import ServicioGastos, AnalizadorGastos
from src.application.strategies import AnalisisTotal, AnalisisPorCategoria
from src.core.exceptions import ServicioError, ValidacionError

class TestServicioGastos(unittest.TestCase):
    
    def setUp(self):
        # Mock de persistencia
        self.mock_persistencia = Mock()
        self.servicio = ServicioGastos(self.mock_persistencia)
        
        # Datos de prueba
        self.usuario = Usuario(id=1, nombre="Usuario Test", email="test@example.com")
        self.categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=1000.0)
    
    def test_registrar_gasto_valido(self):
        gasto = Gasto(
            id=None,
            descripcion="Almuerzo Test",
            monto=300.0,
            fecha=date.today(),
            categoria=self.categoria,
            usuario=self.usuario
        )
        
        # Configurar mock
        self.mock_persistencia.guardar_gasto = Mock()
        
        # Ejecutar
        self.servicio.registrar_gasto(gasto)
        
        # Verificar
        self.mock_persistencia.guardar_gasto.assert_called_once_with(gasto)
    
    def test_registrar_gasto_invalido(self):
        gasto = Gasto(
            id=None,
            descripcion="",  # Descripción vacía - inválida
            monto=300.0,
            fecha=date.today(),
            categoria=self.categoria,
            usuario=self.usuario
        )
        
        with self.assertRaises(ServicioError):
            self.servicio.registrar_gasto(gasto)
    
    def test_obtener_gastos_por_mes(self):
        # Configurar mock
        gastos_mock = []
        self.mock_persistencia.obtener_gastos = Mock(return_value=gastos_mock)
        
        # Ejecutar
        mes = 3
        año = 2024
        resultado = self.servicio.obtener_gastos_por_mes(mes, año, self.usuario)
        
        # Verificar fechas
        fecha_inicio_esperada = date(2024, 3, 1)
        fecha_fin_esperada = date(2024, 4, 1) - timedelta(days=1)  # 31 de marzo
        
        self.mock_persistencia.obtener_gastos.assert_called_once()
        args, _ = self.mock_persistencia.obtener_gastos.call_args
        self.assertEqual(args[0], fecha_inicio_esperada)
        self.assertEqual(args[1], fecha_fin_esperada)
        self.assertEqual(args[2], self.usuario)
        self.assertEqual(resultado, gastos_mock)
    
    def test_obtener_gastos_por_mes_diciembre(self):
        # Configurar mock
        self.mock_persistencia.obtener_gastos = Mock(return_value=[])
        
        # Ejecutar para diciembre
        mes = 12
        año = 2024
        self.servicio.obtener_gastos_por_mes(mes, año, self.usuario)
        
        # Verificar fechas para diciembre
        args, _ = self.mock_persistencia.obtener_gastos.call_args
        fecha_inicio = args[0]
        fecha_fin = args[1]
        
        self.assertEqual(fecha_inicio, date(2024, 12, 1))
        self.assertEqual(fecha_fin, date(2025, 1, 1) - timedelta(days=1))  # 31 de diciembre

class TestAnalizadorGastos(unittest.TestCase):
    
    def setUp(self):
        self.usuario = Usuario(id=1, nombre="Usuario Test", email="test@example.com")
        self.categoria_comida = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=1000.0)
        self.categoria_transporte = Categoria(id=2, nombre="Transporte", presupuesto_mensual=500.0)
        
        # Gastos de prueba
        self.gastos = [
            Gasto(id=1, descripcion="Almuerzo", monto=200.0, fecha=date.today(), 
                categoria=self.categoria_comida, usuario=self.usuario),
            Gasto(id=2, descripcion="Cena", monto=300.0, fecha=date.today(), 
                categoria=self.categoria_comida, usuario=self.usuario),
            Gasto(id=3, descripcion="Bus", monto=50.0, fecha=date.today(), 
                categoria=self.categoria_transporte, usuario=self.usuario),
            Gasto(id=4, descripcion="Taxi", monto=100.0, fecha=date.today(), 
                categoria=self.categoria_transporte, usuario=self.usuario),
        ]
        
        # Estrategias de análisis
        estrategias = [AnalisisTotal(), AnalisisPorCategoria()]
        self.analizador = AnalizadorGastos(estrategias)
    
    def test_calcular_promedios(self):
        promedios = self.analizador.calcular_promedios(self.gastos)
        
        self.assertIn("Alimentación", promedios)
        self.assertIn("Transporte", promedios)
        self.assertEqual(promedios["Alimentación"], 250.0)  # (200 + 300) / 2
        self.assertEqual(promedios["Transporte"], 75.0)     # (50 + 100) / 2
    
    def test_calcular_promedios_sin_gastos(self):
        promedios = self.analizador.calcular_promedios([])
        self.assertEqual(promedios, {})
    
    def test_verificar_alertas_presupuesto_excedido(self):
        # Crear gastos que excedan el presupuesto
        gastos_exceso = [
            Gasto(id=1, descripcion="Supermercado", monto=600.0, fecha=date.today(), 
                categoria=self.categoria_comida, usuario=self.usuario),
            Gasto(id=2, descripcion="Restaurante", monto=500.0, fecha=date.today(), 
                categoria=self.categoria_comida, usuario=self.usuario),
        ]
        
        from src.domain.entities import TipoAlerta
        alertas = self.analizador.verificar_alertas(gastos_exceso)
        
        # Debería generar alerta de presupuesto excedido
        self.assertIn(TipoAlerta.PRESUPUESTO_EXCEDIDO, alertas)
    
    def test_verificar_alertas_nuevo_gasto(self):
        from src.domain.entities import TipoAlerta
        alertas = self.analizador.verificar_alertas(self.gastos)
        
        # Debería generar alerta de nuevo gasto
        self.assertIn(TipoAlerta.NUEVO_GASTO, alertas)
    
    def test_ejecutar_analisis_completo(self):
        resultados = self.analizador.ejecutar_analisis_completo(self.gastos)
        
        # Debería contener resultados de todas las estrategias
        self.assertIn("AnalisisTotal", resultados)
        self.assertIn("AnalisisPorCategoria", resultados)
        
        # Verificar estructura de AnalisisTotal
        analisis_total = resultados["AnalisisTotal"]
        self.assertEqual(analisis_total["total_gastado"], 650.0)
        self.assertEqual(analisis_total["cantidad_gastos"], 4)
        
        # Verificar estructura de AnalisisPorCategoria
        analisis_categoria = resultados["AnalisisPorCategoria"]
        self.assertIn("Alimentación", analisis_categoria)
        self.assertIn("Transporte", analisis_categoria)

class TestEstrategiasAnalisis(unittest.TestCase):
    
    def setUp(self):
        self.usuario = Usuario(id=1, nombre="Usuario Test", email="test@example.com")
        self.categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=1000.0)
        
        self.gastos = [
            Gasto(id=1, descripcion="Almuerzo", monto=200.0, fecha=date.today(), 
                categoria=self.categoria, usuario=self.usuario),
            Gasto(id=2, descripcion="Cena", monto=300.0, fecha=date.today(), 
                categoria=self.categoria, usuario=self.usuario),
        ]
    
    def test_analisis_total(self):
        estrategia = AnalisisTotal()
        resultado = estrategia.analizar(self.gastos)
        
        self.assertEqual(resultado["total_gastado"], 500.0)
        self.assertEqual(resultado["cantidad_gastos"], 2)
        self.assertEqual(resultado["promedio_por_gasto"], 250.0)
        self.assertEqual(resultado["gasto_maximo"], 300.0)
        self.assertEqual(resultado["gasto_minimo"], 200.0)
    
    def test_analisis_por_categoria(self):
        """Test: Estrategia de análisis por categoría"""
        estrategia = AnalisisPorCategoria()
        resultado = estrategia.analizar(self.gastos)
        
        self.assertIn("Alimentación", resultado)
        categoria_info = resultado["Alimentación"]
        self.assertEqual(categoria_info["total"], 500.0)
        self.assertEqual(categoria_info["cantidad"], 2)
        self.assertEqual(categoria_info["porcentaje"], 100.0)  # 100% de los gastos

if __name__ == '__main__':
    # Ejecutar todas las pruebas con verbosidad alta
    unittest.main(verbosity=2)