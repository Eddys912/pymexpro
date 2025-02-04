# 🏭 Gestión de Inventario para Maderería

Sistema para la administración de inventarios en una maderería. Controla empleados, máquinas, materiales y proveedores con seguimiento de costos de producción y generación de reportes.

## 🚀 Características Principales

- 📦 Gestión de inventario con ubicación en almacén.
- 👥 Administración de empleados y roles.
- 🏗️ Control de máquinas y mantenimiento.
- 📊 Generación de reportes en PDF/Excel.
- 🔄 Historial completo de movimientos.

## 🛠 Tecnologías Utilizadas

- **Python 3.11** + **PyQt5** (Interfaz gráfica).
- **MySQL** + **phpMyAdmin** (Base de datos).
- **Pandas** (Análisis de datos) + **FPDF** (Reportes PDF).
- **XAMPP** (Servidor local para MySQL/phpMyAdmin).

## ⚙️ Instalación para Usuarios (Probar el Sistema)

### Requisitos Mínimos

1. [`Python 3.11`](https://www.python.org/downloads/).
2. [`XAMPP`](https://www.apachefriends.org/es/download.html) (Para MySQL y phpMyAdmin).

### Pasos para Configuración

1. **Clona el repositorio** en tu máquina local:
   ```bash
   git clone https://github.com/Eddys912/pymexpro.git
   ```
2. **Accede a la carpeta del proyecto** en el que quieres trabajar:
   ```bash
   cd pymexpro
   ```
3. **Instalar dependencias**:
   ```bash
   pip install pymysql pandas fpdf pyqt5 python-dotenv
   ```
4. **Instalar y configurar XAMPP:**
   - Ejecuta `XAMPP` y activa los módulos `Apache` y `MySQL`.
   - Abre `phpMyAdmin` en: http://localhost/phpmyadmin.
5. **Configurar base de datos:**
   - Crea una nueva base de datos en `phpMyAdmin` llamada pymexpro_db.
   - Ejecuta el archivo `database/init_db.py` desde `vscode`.
6. **Configurar credenciales**
   - Renombrar el archivo `.env.example` a `.env` y configurar las variables
   ```bash
   DB_HOST = "localhost"
   DB_USER = "root"        # Usuario por defecto de XAMPP
   DB_PASSWORD = ""        # Contraseña vacía por defecto
   DB_NAME = "pymexpro_db"
   ```
7. **Ejecutar la aplicación:**
   ```bash
   python main.py  # Reemplaza "main.py" por tu archivo principal
   ```

## 🚀 ¿Cómo Contribuir?

1. **Realiza un Fork** del proyecto haciendo clic en el botón `Fork`.
2. **Realiza los pasos de configuracion.**
3. **Realiza tus cambios**:
   - Guarda los archivos.
   - Crea un commit con una descripción clara:
     ```bash
     git add .
     git commit -m "Descripción de los cambios realizados"
     ```
4. **Envía los cambios** a tu repositorio fork:
   ```bash
   git push origin mi-nueva-funcionalidad
   ```
5. **Abre un Pull Request** 🚀:
   - Dirígete al repositorio original y crea un **Pull Request**.
   - Describe los cambios realizados.
