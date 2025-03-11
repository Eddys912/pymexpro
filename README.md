<div align="center">
  <h1>🏭 PyMexPro - Gestión de Inventario para Maderería 🏭</h1>
  <p>Sistema para la administración de inventarios en una maderería, desarrollado con <strong>Python</strong>, <strong>PyQt6</strong>, <strong>MySQL</strong> y <strong>XAMPP</strong>.</p>

![Python](https://img.shields.io/badge/Python-yellow?logo=python)
![PyQt6](https://img.shields.io/badge/PyQt6-green?logo=qt)
![MySQL](https://img.shields.io/badge/MySQL-005C84?logo=mysql&logoColor=white)
![XAMPP](https://img.shields.io/badge/XAMPP-white?logo=xampp)
</div>

## 🌟 Bienvenido

Este es un sistema de **gestión de inventario** diseñado para administrar eficientemente los materiales, máquinas, empleados, proveedores y clientes de una maderería. Permite controlar el almacenamiento, gestionar compras y ventas, generar reportes y hacer seguimiento de costos de producción.

## 📂 Módulos Principales

| Módulo        | Descripción                                         |
|---------------|-----------------------------------------------------|
| **Inventario**| Control y gestión de materiales y productos.        |
| **Máquinas**  | Gestión de equipos y mantenimiento.                 |
| **Usuarios**  | Administración de empleados, proveedores y clientes.|
| **Compras**   | Registro y control de compras de materiales.        |
| **Ventas**    | Gestión de ventas y clientes.                       |
| **Reportes**  | Generación de informes en PDF y Excel.              |

## 🚀 Instalación y Configuración

### 🛠️ Requisitos Previos

- **Python 3.11** - Instalar desde [Python](https://www.python.org/downloads/).
- **XAMPP** - Para MySQL y phpMyAdmin [XAMPP](https://www.apachefriends.org/es/download.html). 
- **PyQt6 Designer 6.4.2.3.3** - Para la interfaz gráfica.

### 📥 Instalación

1. **Clonar el repositorio en tu máquina local:**
   ```bash
   git clone https://github.com/Eddys912/pymexpro.git
   ```
2. **Acceder a la carpeta del proyecto:**
   ```bash
   cd pymexpro
   ```
3. **Crear y activar un entorno virtual en Visual Studio Code:**
   - Git Bash:
     ```bash
     python -m venv venv
     source venv\Scripts\activate
     ```
4. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Configurar XAMPP y la base de datos:**
   - Ejecuta `XAMPP` y activa los módulos `Apache` y `MySQL`.
   - Abre `phpMyAdmin` en: [http://localhost/phpmyadmin](http://localhost/phpmyadmin).
   - Crea una base de datos llamada `pymexpro_db`.
   - Ejecuta el archivo `database/init_db.py` para inicializar la base de datos.
6. **Configurar credenciales:**
   - Renombrar el archivo `.env.example` a `.env` y configurar las variables:
     ```bash
     DB_HOST = "localhost"
     DB_USER = "root"           # Usuario por defecto de XAMPP
     DB_PASSWORD = ""           # Contraseña vacia por defecto
     DB_NAME = "pymexpro_db"
     ```
7. **Ejecutar la aplicación:**
   ```bash
   python main.py
   ```
## 🚀 ¿Cómo Contribuir?

1. **Realiza un Fork** del proyecto haciendo clic en el botón `Fork`.
2. **Sigue los pasos de Instalación.**
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
