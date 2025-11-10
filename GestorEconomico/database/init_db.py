import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="gestor_economico.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de categorías
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                presupuesto_mensual REAL DEFAULT 0.0,
                color TEXT DEFAULT '#007bff',
                icono TEXT DEFAULT '📁',
                es_personalizada BOOLEAN DEFAULT FALSE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de gastos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                monto REAL NOT NULL,
                fecha DATE NOT NULL,
                categoria_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                moneda TEXT DEFAULT 'ARS',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Insertar usuario por defecto
        cursor.execute('''
            INSERT OR IGNORE INTO usuarios (id, nombre, email) 
            VALUES (1, 'Usuario Gestor Económico', 'usuario@gestoreconomico.com')
        ''')
        
        # Insertar categorías predefinidas
        categorias_predefinidas = [
            ('Alimentación', 15000.0, '#28a745', '🍕'),
            ('Transporte', 8000.0, '#007bff', '🚗'),
            ('Entretenimiento', 5000.0, '#e83e8c', '🎬'),
            ('Salud', 10000.0, '#dc3545', '🏥'),
            ('Educación', 7000.0, '#6f42c1', '📚'),
            ('Vestimenta', 6000.0, '#fd7e14', '👕'),
            ('Hogar', 12000.0, '#20c997', '🏠'),
            ('Servicios', 9000.0, '#6c757d', '💡'),
            ('Viajes', 20000.0, '#17a2b8', '✈️'),
            ('Otros Gastos', 3000.0, '#ffc107', '📦')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO categorias (nombre, presupuesto_mensual, color, icono)
            VALUES (?, ?, ?, ?)
        ''', categorias_predefinidas)
        
        conn.commit()
        conn.close()
        print("✅ Base de datos del Gestor Económico inicializada correctamente")

if __name__ == "__main__":
    db_manager = DatabaseManager()