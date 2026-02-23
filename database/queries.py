from database.connection import DatabaseConnection

class DatabaseQueries:
    
    @staticmethod
    def execute_query(query, params=None, fetch=True):
        connection = None
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                connection.commit()
                cursor.close()
                return True
                
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                DatabaseConnection.return_connection(connection)
    
    @staticmethod
    def get_all_tables():
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        """
        return DatabaseQueries.execute_query(query)
    
    @staticmethod
    def get_table_data(table_name, limit=100):
        query = f"SELECT * FROM {table_name} LIMIT %s"
        return DatabaseQueries.execute_query(query, (limit,))
