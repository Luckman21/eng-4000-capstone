import sqlite3

# Connect to the database (it will create the file if it doesn't exist)
conn = sqlite3.connect('../capstone_db.db')
cursor = conn.cursor()


# Material Type Creation

cursor.execute('''
CREATE TABLE material_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL UNIQUE
)
''')

# Material Table Creation
# autoincrement allows us to consistently increment each ID by 1

cursor.execute('''
CREATE TABLE materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colour TEXT NOT NULL,
    name TEXT NOT NULL, 
    mass FLOAT NOT NULL,
    material_type_id INTEGER,
    FOREIGN KEY (material_type_id) REFERENCES material_type(id) ON DELETE CASCADE
)
''')

# Shelf Table
cursor.execute('''
CREATE TABLE shelfs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    humidity_pct REAL NOT NULL,
    temperature_cel REAL NOT NULL 
)
''')

# User Table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL, 
    email TEXT NOT NULL UNIQUE,
    user_type_id INTEGER,
    FOREIGN KEY (user_type_id) REFERENCES user_type(id) ON DELETE SET NULL
)
''')

# User Type Table
cursor.execute('''
CREATE TABLE user_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL UNIQUE
)
''')

conn.commit()
conn.close()
