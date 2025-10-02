import mysql.connector
from mysql.connector import Error

def connect_db():
    """
    Establishes a connection to the MySQL database.
    
    Returns:
        connection (mysql.connector.connection.MySQLConnection): 
            MySQL database connection object if successful, else None.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin123",  # 🔑 Replace with your actual MySQL root password
            database="fletapp"
        )
        if connection.is_connected():
            print("✅ Successfully connected to the database.")
            return connection
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return None

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        conn.close()
        print("🔒 Connection closed.")