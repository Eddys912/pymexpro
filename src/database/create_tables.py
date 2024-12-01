def drop_tables(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS production_reports")
        cursor.execute("DROP TABLE IF EXISTS inventory")
        cursor.execute("DROP TABLE IF EXISTS managers")
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute("DROP TABLE IF EXISTS machines")
        cursor.execute("DROP TABLE IF EXISTS managers")
        conn.commit()
        print("Tablas eliminadas")
    except Exception as e:
        print(f"Error al eliminar las tabla {e}")
    finally:
        cursor.close()


def create_table_users(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute(
            """
            CREATE TABLE users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                gender VARCHAR(10),
                username VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                phone VARCHAR(15),
                role VARCHAR(50) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                birth_date TIMESTAMP NULL,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
        print("Tabla 'users' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla 'users': {e}")
    finally:
        cursor.close()


def create_table_products(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute(
            """
            CREATE TABLE products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(100) NOT NULL UNIQUE,
                description TEXT,
                production_cost DECIMAL(10,2) NOT NULL,
                sale_price DECIMAL(10,2) NOT NULL,
                stock INT DEFAULT 0,
                category VARCHAR(50),
                creation_date DATE NOT NULL,
                is_active BOOLEAN DEFAULT TRUE
            )
        """
        )
        conn.commit()
        print("Tabla 'products' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla 'products': {e}")
    finally:
        cursor.close()


def create_table_machines(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS machines")
        cursor.execute(
            """
            CREATE TABLE machines (
                machine_id INT AUTO_INCREMENT PRIMARY KEY,
                machine_name VARCHAR(100) NOT NULL UNIQUE,
                type VARCHAR(50) NOT NULL,
                production_capacity INT,
                status VARCHAR(20) DEFAULT 'Operativa',
                installation_date DATE NOT NULL,
                last_maintenance DATE,
                responsible VARCHAR(100),
                is_active BOOLEAN DEFAULT TRUE
            )
        """
        )
        conn.commit()
        print("Tabla 'machines' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla 'machines': {e}")
    finally:
        cursor.close()


def create_table_managers(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS managers")
        cursor.execute(
            """
            CREATE TABLE managers (
                manager_id INT PRIMARY KEY,
                shift VARCHAR(20) NOT NULL,
                responsible_area VARCHAR(100) NOT NULL,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_manager_user FOREIGN KEY (manager_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """
        )
        conn.commit()
        print("Tabla 'managers' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla 'managers': {e}")
    finally:
        cursor.close()


def create_table_production_reports(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS production_reports")
        cursor.execute(
            """
            CREATE TABLE production_reports (
                report_id INT AUTO_INCREMENT PRIMARY KEY,
                manager_id INT NOT NULL,
                product_id INT NOT NULL,
                machine_id INT NOT NULL,
                produced_quantity INT NOT NULL,
                defective_quantity INT DEFAULT 0,
                production_date DATE NOT NULL,
                comments TEXT,
                CONSTRAINT fk_report_manager FOREIGN KEY (manager_id) REFERENCES managers(manager_id) ON DELETE CASCADE,
                CONSTRAINT fk_report_product FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
                CONSTRAINT fk_report_machine FOREIGN KEY (machine_id) REFERENCES machines(machine_id) ON DELETE CASCADE
            )
        """
        )
        conn.commit()
        print("Tabla 'production_reports' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla 'production_reports': {e}")
    finally:
        cursor.close()


def create_table_inventory(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS inventory")
        cursor.execute(
            """
            CREATE TABLE inventory (
                inventory_id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                entry_quantity INT DEFAULT 0,
                exit_quantity INT DEFAULT 0,
                movement_date DATE NOT NULL,
                movement_type VARCHAR(20) NOT NULL,
                responsible VARCHAR(100) NOT NULL,
                observations TEXT,
                CONSTRAINT fk_inventory_product FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
            )
        """
        )
        conn.commit()
        print("Tabla 'inventory' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla 'inventory': {e}")
    finally:
        cursor.close()
