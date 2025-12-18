import pytest
from config.database import DatabaseConfig

@pytest.fixture(scope='function')
def db_connection():
    """
    Fixture que proporciona conexión a DB con auto-rollback.
    Cada test corre en su propia transacción que se revierte al final.
    """
    conn = DatabaseConfig.get_connection()
    conn.autocommit = False
    
    yield conn
    
    # Rollback automático después de cada test
    conn.rollback()
    conn.close()


@pytest.fixture(scope='session', autouse=True)
def setup_test_database():
    """
    Setup de schema de DB antes de todos los tests.
    Crea tablas necesarias una sola vez.
    """
    conn = DatabaseConfig.get_connection()
    cursor = conn.cursor()
    
    # Crear tabla users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Crear tabla orders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            product_name VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            total_price DECIMAL(10,2) NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    yield
    
    # Cleanup: drop tables después de todos los tests
    conn = DatabaseConfig.get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS orders CASCADE")
    cursor.execute("DROP TABLE IF EXISTS users CASCADE")
    conn.commit()
    cursor.close()
    conn.close()
    