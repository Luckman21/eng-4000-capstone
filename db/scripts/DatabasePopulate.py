import sqlite3

# Connecting to the database
conn = sqlite3.connect('../capstone_db.db')
cursor = conn.cursor()

# Populating the different material types given by Pantheon
material_type = [
    ("FDM"),
    ("SLA"),
    ("PLA"),
    ("Silk PLA"),
    ("PETG"),
    ("TPU"),
    ("ABS"),
    ("ASA"),
    ("PAHT CF"),
    ("NYLON")
]

cursor.executemany("INSERT INTO material_types (name) VALUES (?)", material_type) # inserting the names into material type class

# Populating the different materials that are connected with each material type
material = [
    ("Black", "Smokey Black", 3.2, 1),
    ("Blue", "Sky Blue", 100.0, 1),
    ("Green", "Mother Earth", 100.0, 2),
    ("Red", "Sunset", 300.4, 2),
    ("Yellow", "Sunrise", 2.0, 3)
    ("White", "Surface Moon", 49.0 ,3),
    ("Brown", "Dirt Ground", 1000.0, 4),
    ("Teal", "Seaweed", 50.3, 4),
    ("Silver", "Starry Night", 50.3, 5),
    ("Purple", "Barney", 50.3, 5),
    ("Gray", "Cloudy Day", 50.3, 6),
    ("Orange", "Pumpkin", 50.3, 6),
    ("Maroon", "Oakwood", 50.3, 7),
    ("Aquamarine", "Poolside", 505.3, 7),
    ("Lime", "Sprite", 30.3, 8),
    ("Crimson", "Lobster", 70.6, 8),
    ("Pink", "Barbie", 50.0, 9),
    ("Magenta", "Uniqua", 49.9, 9),
    ("Gold", "Olympics", 50.3, 10),
    ("Black", "Night Sky", 50.3, 10)

]

cursor.executemany("INSERT INTO materials (colour, name, mass, material_type_id) VALUES (?, ?, ?, ?)", material) # This will insert the material values into the material class

# Populating different shelves with different humidity and temperature values
shelves = [
    (935, 13.5),
    (950, 18),
    (1050, 24.5),
    (1025, 22.5),
    (1100, 26)
    (800, 10),
    (1200, 29),
    (1000, 22),
    (975, 20),
    (850, 11.5)
]

cursor.executemany("INSERT INTO shelfs (humidity_pct, temp_cel) VALUES (?, ?)", shelves) # Inserting shelf values into the class

# Populating with different user types
user_type = [
    ("Admin"),
    ("Super_Admin")
]

cursor.executemany("INSERT INTO user_types (name) VALUES (?)", user_type) # Inserting the two user types into the user_type class

# Populating with multiple users to test our users table
users = [
    ("james7", "jones7788", "jj7@gmail.com", 2),
    ("hugh_55", "pecan7275", "hugh_p55@hotmail.com", 1),
    ("scream777", "scary4578", "scream33@hotmail.com", 1),
    ("water_123", "Gucci2001", "water7@gmail.com", 2),
    ("peter_g7", "griff4508", "peterg@hotmail.com", 2),
    ("jake_99", "laugh0910", "jake_p@gmail.com", 1),
    ("josh_z", "sides2525", "josh_23@gmail.com", 2),
    ("simonM", "bball0710", "simon_M@hotmail.com", 1),
    ("Tyler23", "Igors1998", "TytheC@gmail.com", 2),
    ("Drizzy6", "Drake2334", "Drake23@hotmail.com", 1)
]

cursor.executemany("INSERT INTO users (username, password, email, user_type_id) VALUES (?, ?, ?, ?)", users) # inserting the values of the user into the user class

conn.commit()
conn.close()