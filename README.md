# Najah Graduate Studies Chatbot

## Project Structure

```
.
├── config/
│   └── database.py          # Database configuration
├── database/
│   ├── connection.py        # Database connection pool management
│   └── queries.py           # Database query functions
├── .env                     # Environment variables (not in git)
├── .env.example            # Example environment file
├── requirements.txt        # Python dependencies
└── test_connection.py      # Test database connection
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create .env file:
```bash
cp .env.example .env
```

3. Add your database password to .env file:
```
DB_PASSWORD=your_actual_password
```

4. Test connection:
```bash
python test_connection.py
```

## Usage

```python
from database.queries import DatabaseQueries

# Get all tables
tables = DatabaseQueries.get_all_tables()

# Get data from specific table
data = DatabaseQueries.get_table_data('your_table_name')

# Execute custom query
result = DatabaseQueries.execute_query("SELECT * FROM your_table WHERE id = %s", (1,))
```
