import unittest
from datetime import date
import sys
import os

# Agregar el directorio src al path para las importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.domain.entities import Usuario, Categoria, Gasto, Moneda
from src.core.exceptions import ValidacionError

class TestUsuario(unittest.TestCase):
    
    def test_usuario_valido(self):
        usuario = Usuario(id=1, nombre="Juan Pérez", email="juan@example.com")
        self.assertTrue(usuario.validar())
    
    def test_usuario_nombre_vacio(self):
        usuario = Usuario(id=1, nombre="", email="juan@example.com")
        with self.assertRaises(ValidacionError):
            usuario.validar()
    
    def test_usuario_nombre_espacios(self):
        usuario = Usuario(id=1, nombre="   ", email="juan@example.com")
        with self.assertRaises(ValidacionError):
            usuario.validar()
    
    def test_usuario_email_invalido(self):
        usuario = Usuario(id=1, nombre="Juan Pérez", email="email-invalido")
        with self.assertRaises(ValidacionError):
            usuario.validar()
    
    def test_usuario_email_sin_arroba(self):
        usuario = Usuario(id=1, nombre="Juan Pérez", email="juanexample.com")
        with self.assertRaises(ValidacionError):
            usuario.validar()
    
    def test_usuario_repr(self):
        usuario = Usuario(id=1, nombre="Juan Pérez", email="juan@example.com")
        self.assertIn("Juan Pérez", str(usuario))
        self.assertIn("juan@example.com", str(usuario))

class TestCategoria(unittest.TestCase):
    
    def test_categoria_valida(self):
        categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=1000.0)
        self.assertTrue(categoria.validar())
    
    def test_categoria_nombre_vacio(self):
        categoria = Categoria(id=1, nombre="", presupuesto_mensual=1000.0)
        with self.assertRaises(ValidacionError):
            categoria.validar()
    
    def test_categoria_presupuesto_negativo(self):
        categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=-100.0)
        with self.assertRaises(ValidacionError):
            categoria.validar()
    
    def test_categoria_presupuesto_cero(self):
        categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=0.0)
        self.assertTrue(categoria.validar())
    
    def test_categoria_repr(self):
        categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=1500.0, icono="🍕")
        self.assertIn("Alimentación", str(categoria))
        self.assertIn("1500.00", str(categoria))

class TestGasto(unittest.TestCase):
    
    def setUp(self):
        self.usuario = Usuario(id=1, nombre="Usuario Test", email="test@example.com")
        self.categoria = Categoria(id=1, nombre="Alimentación", presupuesto_mensual=1000.0)
    
    def test_gasto_valido(self):
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
    
    def test_moneda_valores(self):
        self.assertEqual(Moneda.ARS.value, "ARS")
        self.assertEqual(Moneda.USD.value, "USD")
        self.assertEqual(Moneda.EUR.value, "EUR")
    
    def test_moneda_str(self):
        self.assertEqual(str(Moneda.ARS), "ARS")
        self.assertEqual(str(Moneda.USD), "USD")

if __name__ == '__main__':
    # Ejecutar todas las pruebas
    unittest.main(verbosity=2)