import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'dpg-d690u1a48b3s73ato6g0-a.oregon-postgres.render.com'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'najah_gradbot_database'),
    'user': os.getenv('DB_USER', 'najah_gradbot_database_user'),
    'password': os.getenv('DB_PASSWORD', '')
}
