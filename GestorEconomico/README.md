📊 Gestor Económico
Sistema de Gestión de Gastos Personales - Una aplicación de escritorio desarrollada en Python para el control y análisis de tus finanzas personales.


🚀 Características Principales
💰 Gestión de Gastos
Registro inteligente de gastos con descripción, monto, categoría y fecha

Validación automática de datos ingresados

Interfaz intuitiva para agregar, visualizar y eliminar gastos

Categorización flexible con 10 categorías predefinidas

📈 Análisis y Reportes
Reportes mensuales detallados con desglose por categoría

Comparativa entre meses con análisis de tendencias

Estadísticas visuales de distribución de gastos

Resumen ejecutivo con información clave

📤 Exportación de Datos
Exportación a Excel en formato CSV compatible

Estructura optimizada para apertura directa en Excel

Formato español con separadores y decimales correctos

🛠️ Tecnologías Utilizadas
Python 3.8+ - Lenguaje principal

Tkinter - Interfaz gráfica

SQLite - Base de datos local

Arquitectura en Capas - Diseño modular y mantenible

Principios SOLID - Código limpio y extensible

📦 Instalación
Prerrequisitos
Python 3.8 o superior

pip (gestor de paquetes de Python)

Pasos de Instalación
Clonar o descargar el proyecto

bash
git clone <url-del-repositorio>
cd GestorEconomico
Verificar la estructura del proyecto

text
GestorEconomico/
├── main.py
├── database/
├── src/
└── tests/
Ejecutar la aplicación

bash
python main.py
🎯 Uso de la Aplicación
Primera Ejecución
La aplicación crea automáticamente la base de datos

Se inicializan 10 categorías predefinidas

Se crea un usuario por defecto

Gestión de Gastos
Agregar gasto: Completa el formulario con descripción, monto, categoría y fecha

Visualizar gastos: Consulta la lista de gastos del mes actual

Eliminar gasto: Selecciona un gasto y haz clic en "Eliminar"

Análisis de Datos
Reporte mensual: Genera un análisis completo del mes actual

Comparar meses: Compara gastos con el mes anterior

Resumen ejecutivo: Vista rápida de estadísticas clave

Exportación
Exportar a Excel: Haz clic en "Exportar Excel" para guardar tus datos

Abrir en Excel: El archivo CSV generado se abre directamente en Excel

🏗️ Arquitectura del Proyecto
text
GestorEconomico/
├── 📁 database/          # Inicialización de base de datos
├── 📁 src/              # Código fuente principal
│   ├── 📁 core/         # Excepciones y componentes base
│   ├── 📁 domain/       # Entidades e interfaces
│   ├── 📁 application/  # Servicios y lógica de negocio
│   ├── 📁 infrastructure/ # Persistencia y notificaciones
│   └── 📁 presentation/ # Interfaz de usuario
├── 📁 tests/            # Pruebas unitarias
└── 📄 main.py          # Punto de entrada
📊 Categorías Predefinidas
La aplicación incluye 10 categorías organizadas con presupuestos sugeridos:

Categoría	Presupuesto Sugerido	Icono
🍕 Alimentación	$15,000	🍕
🚗 Transporte	$8,000	🚗
🎬 Entretenimiento	$5,000	🎬
🏥 Salud	$10,000	🏥
📚 Educación	$7,000	📚
👕 Vestimenta	$6,000	👕
🏠 Hogar	$12,000	🏠
💡 Servicios	$9,000	💡
✈️ Viajes	$20,000	✈️
📦 Otros Gastos	$3,000	📦


🔧 Personalización
Agregar Nuevas Categorías
La aplicación permite crear categorías personalizadas con:

Nombre personalizado

Presupuesto mensual

Color identificativo

Icono representativo



🐛 Solución de Problemas
Error al Iniciar
Verificar que Python 3.8+ esté instalado

Asegurar que todos los archivos estén en la ubicación correcta

Ejecutar desde la carpeta raíz del proyecto

Problemas con la Base de Datos
La aplicación crea automáticamente la base de datos en la primera ejecución

Verificar permisos de escritura en el directorio

Exportación a Excel
El archivo CSV se abre automáticamente con Excel si está instalado

Usar "Abrir con" → Excel si no se abre directamente

📈 Beneficios de Usar Gestor Económico
✅ Control total sobre tus finanzas personales

✅ Toma decisiones informadas basadas en datos reales

✅ Identifica patrones de gasto y oportunidades de ahorro

✅ Planificación futura basada en historial

✅ Interfaz simple sin curva de aprendizaje