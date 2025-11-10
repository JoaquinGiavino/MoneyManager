import unittest
from datetime import date
import sys
import os

# Agregar el directorio src al path para las importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.domain.entities import Usuario, Categoria, Gasto, Moneda
from src.core.exceptions import ValidacionError

class TestUsuario(unittest.TestCase):
    """Pruebas unitarias para la entidad Usuario del Gestor Económico"""
    
    def test_usuario_valido(self):
        """Test: Usuario con datos válidos debe pasar validación"""
        usuario = Usuario(id=1, nombre="Juan Pérez", email="juan@example.com")
        self.assertTrue(usuario.validar())
    
    def test_usuario_nombre_vacio(self):
        """Test: Usuario con nombre vacío debe lanzar ValidacionError"""
        usuario = Usuario(id=1, nombre="", email="juan@example.com")
        with self.assertRaises(ValidacionError):
            usuario.validar()
    
    def test_usuario_nombre_espacios(self):
        """Test: Usuario con nombre de solo espacios debe lanzar ValidacionError"""
        usuario = Usuario(id=1, nombre="   ", email="juan@example.com")
        with self.assertRaises(ValidacionError):
            usuario.validar()
    
    def test_usuario_email_invalido(self):
        """Test: Usuario con email inválido debe lanzar ValidacionError"""
        usuario = Usuario(id=1, nombre="Juan Pérez", email="email-invalido")
        with self.assertRaises(ValidacionError):
            usuario.validar()
    
    def test_usuario_email_sin_arroba(self):
        """Test: Usuario con email sin @ debe lanzar ValidacionError"""
        usuario = Usuario(id=1, nombre="Juan Pérez", email="juanexample.com")
        with self.assertRaises(ValidacionError):
            usuario.validar()
    
    def test_usuario_repr(self):
        """Test: Representación en string del usuario"""
        usuario = Usuario(id=1, nombre="Juan Pérez", email="juan@example.com")
        self.assertIn("Juan Pérez", str(usuario))
        self.assertIn("juan@example.com", str(usuario))

class TestCategoria(unittest.TestCase):
    """Pruebas unitarias para la entidad Categoria del Gestor Económico"""
    
    def test_categoria_valida(self):
        """Test: Categoría con datos válidos debe pasar validación"""
        categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=1000.0)
        self.assertTrue(categoria.validar())
    
    def test_categoria_nombre_vacio(self):
        """Test: Categoría con nombre vacío debe lanzar ValidacionError"""
        categoria = Categoria(id=1, nombre="", presupuesto_mensual=1000.0)
        with self.assertRaises(ValidacionError):
            categoria.validar()
    
    def test_categoria_presupuesto_negativo(self):
        """Test: Categoría con presupuesto negativo debe lanzar ValidacionError"""
        categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=-100.0)
        with self.assertRaises(ValidacionError):
            categoria.validar()
    
    def test_categoria_presupuesto_cero(self):
        """Test: Categoría con presupuesto cero debe pasar validación"""
        categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=0.0)
        self.assertTrue(categoria.validar())
    
    def test_categoria_repr(self):
        """Test: Representación en string de la categoría"""
        categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=1500.0, icono="🍕")
        self.assertIn("Alimentación", str(categoria))
        self.assertIn("1500.00", str(categoria))

class TestGasto(unittest.TestCase):
    """Pruebas unitarias para la entidad Gasto del Gestor Económico"""
    
    def setUp(self):
        """Configuración inicial para las pruebas de gastos"""
        self.usuario = Usuario(id=1, nombre="Usuario Test", email="test@example.com")
        self.categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=1000.0)
    
    def test_gasto_valido(self):
        """Test: Gasto con datos válidos debe pasar validación"""
        gasto = Gasto(
            id=1, 
            descripcion="Almuerzo en restaurante", 
            monto=500.0, 
            fecha=date.today(),
            categoria=self.categoria,
            usuario=self.usuario
        )
        self.assertTrue(gasto.validar())
    
    def test_gasto_descripcion_vacia(self):
        """Test: Gasto con descripción vacía debe lanzar ValidacionError"""
        gasto = Gasto(
            id=1, 
            descripcion="", 
            monto=500.0, 
            fecha=date.today(),
            categoria=self.categoria,
            usuario=self.usuario
        )
        with self.assertRaises(ValidacionError):
            gasto.validar()
    
    def test_gasto_monto_cero(self):
        """Test: Gasto con monto cero debe lanzar ValidacionError"""
        gasto = Gasto(
            id=1, 
            descripcion="Almuerzo", 
            monto=0.0, 
            fecha=date.today(),
            categoria=self.categoria,
            usuario=self.usuario
        )
        with self.assertRaises(ValidacionError):
            gasto.validar()
    
    def test_gasto_monto_negativo(self):
        """Test: Gasto con monto negativo debe lanzar ValidacionError"""
        gasto = Gasto(
            id=1, 
            descripcion="Almuerzo", 
            monto=-100.0, 
            fecha=date.today(),
            categoria=self.categoria,
            usuario=self.usuario
        )
        with self.assertRaises(ValidacionError):
            gasto.validar()
    
    def test_gasto_fecha_futura(self):
        """Test: Gasto con fecha futura debe lanzar ValidacionError"""
        fecha_futura = date.today().replace(year=date.today().year + 1)
        gasto = Gasto(
            id=1, 
            descripcion="Almuerzo", 
            monto=500.0, 
            fecha=fecha_futura,
            categoria=self.categoria,
            usuario=self.usuario
        )
        with self.assertRaises(ValidacionError):
            gasto.validar()
    
    def test_gasto_repr(self):
        """Test: Representación en string del gasto"""
        gasto = Gasto(
            id=1, 
            descripcion="Almuerzo", 
            monto=500.0, 
            fecha=date.today(),
            categoria=self.categoria,
            usuario=self.usuario
        )
        self.assertIn("Almuerzo", str(gasto))
        self.assertIn("500.00", str(gasto))

class TestMoneda(unittest.TestCase):
    """Pruebas unitarias para el enum Moneda del Gestor Económico"""
    
    def test_moneda_valores(self):
        """Test: Verificar valores del enum Moneda"""
        self.assertEqual(Moneda.ARS.value, "ARS")
        self.assertEqual(Moneda.USD.value, "USD")
        self.assertEqual(Moneda.EUR.value, "EUR")
    
    def test_moneda_str(self):
        """Test: Representación en string de Moneda"""
        self.assertEqual(str(Moneda.ARS), "ARS")
        self.assertEqual(str(Moneda.USD), "USD")

if __name__ == '__main__':
    # Ejecutar todas las pruebas
    unittest.main(verbosity=2)