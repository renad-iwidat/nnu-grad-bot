from database.connection import DatabaseConnection
from database.queries import DatabaseQueries

def test_database_connection():
    try:
        print("Testing database connection...")
        
        tables = DatabaseQueries.get_all_tables()
        print(f"\nFound {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        print("\nConnection successful!")
        return True
        
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False
    finally:
        DatabaseConnection.close_all_connections()

if __name__ == "__main__":
    test_database_connection()
