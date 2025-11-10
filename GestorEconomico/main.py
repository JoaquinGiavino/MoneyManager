import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.init_db import DatabaseManager
from src.presentation.gui import GestionGastosApp

def main():
    print("🚀 Iniciando Sistema de Gestión de Gastos...")
    
    try:
        db_manager = DatabaseManager()
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        return
    
    try:
        app = GestionGastosApp()
        print("✅ Aplicación iniciada correctamente")
        app.run()
    except Exception as e:
        print(f"❌ Error al iniciar aplicación: {e}")

if __name__ == "__main__":
    main()