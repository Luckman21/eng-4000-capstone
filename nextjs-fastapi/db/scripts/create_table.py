import psycopg  # type: ignore # If this fails, install it using: pip install psycopg

# Database connection details
DATABASE_URL = "postgresql://postgres:0000@localhost/capstone_db"

# Connect to PostgreSQL
conn = psycopg.connect(DATABASE_URL)
cursor = conn.cursor()

# Material Type Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS material_types (
    id SERIAL PRIMARY KEY,
    type_name TEXT NOT NULL UNIQUE
)
''')

# Warning

cursor.execute('''
CREATE TABLE IF NOT EXISTS warnings (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT
)
''')

# Shelf Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS shelfs (
    id SERIAL PRIMARY KEY,
    humidity_pct DOUBLE PRECISION NOT NULL,
    temperature_cel DOUBLE PRECISION NOT NULL 
)
''')

# Material Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS materials (
    id SERIAL PRIMARY KEY,
    colour TEXT NOT NULL,
    supplier_link TEXT NOT NULL, 
    mass DOUBLE PRECISION NOT NULL,
    material_type_id INTEGER REFERENCES material_types(id) ON DELETE CASCADE,
    shelf_id INTEGER REFERENCES shelfs(id) ON DELETE CASCADE
)
''')

# User Type Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_types (
    id SERIAL PRIMARY KEY,
    type_name TEXT NOT NULL UNIQUE
)
''')

# User Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL, 
    email TEXT NOT NULL UNIQUE,
    user_type_id INTEGER REFERENCES user_types(id) ON DELETE SET NULL
)
''')

# Commit and close the connection
conn.commit()
cursor.close()
conn.close()
