import sqlalchemy
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

class DatabaseManager:
    def __init__(self, dialect, connection_string):
        if dialect == 'mysql':
            # Parse the connection string manually
            parts = connection_string.split('://', 1)[1].split('@')
            user_pass = parts[0].split(':')
            host_port_db = parts[1].split('/')
            
            user = user_pass[0]
            password = quote_plus(user_pass[1])  # URL encode the password
            host_port = host_port_db[0].split(':')
            host = host_port[0]
            port = host_port[1] if len(host_port) > 1 else '3306'
            database = host_port_db[1]
            
            # Reconstruct the connection string
            connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        
        self.engine = create_engine(connection_string)

    def execute_query(self, query):
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            return [dict(row) for row in result]

    def test_connection(self):
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False
