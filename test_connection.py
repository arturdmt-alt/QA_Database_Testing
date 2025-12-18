from config.database import DatabaseConfig

try:
    conn = DatabaseConfig.get_connection()
    print("Conexión exitosa")
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"Version: {version[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
    