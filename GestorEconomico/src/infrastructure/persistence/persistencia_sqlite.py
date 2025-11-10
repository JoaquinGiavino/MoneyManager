import sqlite3
from datetime import date
from typing import List, Optional
from src.domain.entities import Usuario, Gasto, Categoria, Moneda
from src.domain.interfaces import IPersistenciaLocal
from src.core.exceptions import PersistenciaError

class PersistenciaSQLite(IPersistenciaLocal):
    def __init__(self, db_path: str = "gestor_economico.db"):  # Cambiado a gestor_economico.db
        self.db_path = db_path
    
    def _get_connection(self) -> sqlite3.Connection:
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            raise PersistenciaError(f"Error de conexión: {str(e)}")
    
    def guardar_gasto(self, gasto: Gasto) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO gastos (descripcion, monto, fecha, categoria_id, usuario_id, moneda)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                gasto.descripcion,
                gasto.monto,
                gasto.fecha.isoformat(),
                gasto.categoria.id,
                gasto.usuario.id,
                gasto.moneda.value
            ))
            
            conn.commit()
            print(f"✅ Gasto guardado: {gasto.descripcion} - ${gasto.monto:.2f}")
            
        except sqlite3.Error as e:
            conn.rollback()
            raise PersistenciaError(f"Error al guardar gasto: {str(e)}")
        finally:
            conn.close()
    
    def obtener_gastos(self, fecha_inicio: date, fecha_fin: date, usuario: Usuario) -> List[Gasto]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT g.id, g.descripcion, g.monto, g.fecha, g.moneda,
                    c.id, c.nombre, c.presupuesto_mensual, c.color, c.icono, c.es_personalizada,
                    u.id, u.nombre, u.email
                FROM gastos g
                JOIN categorias c ON g.categoria_id = c.id
                JOIN usuarios u ON g.usuario_id = u.id
                WHERE g.fecha BETWEEN ? AND ? AND g.usuario_id = ?
                ORDER BY g.fecha DESC, g.id DESC
            ''', (fecha_inicio.isoformat(), fecha_fin.isoformat(), usuario.id))
            
            gastos = []
            for row in cursor.fetchall():
                categoria = Categoria(
                    id=row[5], 
                    nombre=row[6], 
                    presupuesto_mensual=row[7],
                    color=row[8], 
                    icono=row[9], 
                    es_personalizada=bool(row[10])
                )
                
                usuario_obj = Usuario(id=row[11], nombre=row[12], email=row[13])
                
                gasto = Gasto(
                    id=row[0], 
                    descripcion=row[1], 
                    monto=row[2],
                    fecha=date.fromisoformat(row[3]), 
                    categoria=categoria,
                    usuario=usuario_obj, 
                    moneda=Moneda(row[4])
                )
                
                gastos.append(gasto)
            
            print(f"✅ Obtenidos {len(gastos)} gastos del período {fecha_inicio} a {fecha_fin}")
            return gastos
            
        except sqlite3.Error as e:
            raise PersistenciaError(f"Error al obtener gastos: {str(e)}")
        finally:
            conn.close()
    
    def obtener_categorias(self) -> List[Categoria]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, nombre, presupuesto_mensual, color, icono, es_personalizada 
                FROM categorias 
                ORDER BY es_personalizada, nombre
            ''')
            
            categorias = []
            for row in cursor.fetchall():
                categoria = Categoria(
                    id=row[0], 
                    nombre=row[1], 
                    presupuesto_mensual=row[2],
                    color=row[3], 
                    icono=row[4], 
                    es_personalizada=bool(row[5])
                )
                categorias.append(categoria)
            
            print(f"✅ Obtenidas {len(categorias)} categorías")
            return categorias
            
        except sqlite3.Error as e:
            raise PersistenciaError(f"Error al obtener categorías: {str(e)}")
        finally:
            conn.close()
    
    def guardar_categoria(self, categoria: Categoria) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            if categoria.id:
                cursor.execute('''
                    UPDATE categorias 
                    SET nombre=?, presupuesto_mensual=?, color=?, icono=?, es_personalizada=?
                    WHERE id=?
                ''', (
                    categoria.nombre, categoria.presupuesto_mensual,
                    categoria.color, categoria.icono, categoria.es_personalizada,
                    categoria.id
                ))
                print(f"✅ Categoría actualizada: {categoria.nombre}")
            else:
                cursor.execute('''
                    INSERT INTO categorias (nombre, presupuesto_mensual, color, icono, es_personalizada)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    categoria.nombre, categoria.presupuesto_mensual,
                    categoria.color, categoria.icono, categoria.es_personalizada
                ))
                print(f"✅ Nueva categoría creada: {categoria.nombre}")
            
            conn.commit()
            
        except sqlite3.Error as e:
            conn.rollback()
            raise PersistenciaError(f"Error al guardar categoría: {str(e)}")
        finally:
            conn.close()
    
    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT id, nombre, email FROM usuarios WHERE email = ?', (email,))
            row = cursor.fetchone()
            
            if row:
                usuario = Usuario(id=row[0], nombre=row[1], email=row[2])
                print(f"✅ Usuario encontrado: {usuario.nombre}")
                return usuario
            
            print("⚠️ Usuario no encontrado")
            return None
            
        except sqlite3.Error as e:
            raise PersistenciaError(f"Error al obtener usuario: {str(e)}")
        finally:
            conn.close()

    # 🔥 MÉTODO CORREGIDO - BIEN INDENTADO
    def eliminar_gasto(self, gasto_id: int, usuario: Usuario) -> bool:
        """Eliminar un gasto del Gestor Económico"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar que el gasto pertenece al usuario antes de eliminar
            cursor.execute('SELECT id FROM gastos WHERE id = ? AND usuario_id = ?', 
                        (gasto_id, usuario.id))
            gasto_existente = cursor.fetchone()
            
            if not gasto_existente:
                print(f"⚠️ Gasto {gasto_id} no encontrado o no pertenece al usuario")
                return False
            
            # Obtener información del gasto para el log
            cursor.execute('''
                SELECT g.descripcion, g.monto, c.nombre 
                FROM gastos g 
                JOIN categorias c ON g.categoria_id = c.id 
                WHERE g.id = ? AND g.usuario_id = ?
            ''', (gasto_id, usuario.id))
            
            info_gasto = cursor.fetchone()
            descripcion = info_gasto[0] if info_gasto else "Desconocido"
            monto = info_gasto[1] if info_gasto else 0
            categoria = info_gasto[2] if info_gasto else "Desconocida"
            
            # Eliminar el gasto
            cursor.execute('DELETE FROM gastos WHERE id = ? AND usuario_id = ?', 
                        (gasto_id, usuario.id))
            
            conn.commit()
            filas_afectadas = cursor.rowcount
            
            if filas_afectadas > 0:
                print(f"✅ Gasto eliminado: '{descripcion}' - ${monto:.2f} ({categoria})")
                return True
            else:
                print(f"⚠️ No se pudo eliminar el gasto {gasto_id}")
                return False
                
        except sqlite3.Error as e:
            conn.rollback()
            raise PersistenciaError(f"Error al eliminar gasto: {str(e)}")
        finally:
            conn.close()