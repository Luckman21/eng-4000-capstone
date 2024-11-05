import sqlite3

conn = sqlite3.connect('../capstone_db.db')
cursor = conn.cursor()

material_type = [
    (1, "FDM"),
    (2, "SLA"),
    (3, "PLA"),
    (4, "Silk PLA"),
    (5, "PETG"),
    (6, "TPU"),
    (7, "ABS"),
    (8, "ASA"),
    (9, "PAHT CF"),
    (10, "NYLON")
]

cursor.executemany("INSERT INTO material_type (id_type, name) VALUES (?, ?)", material_type)

material = [
    (1, "Black", "Smokey Black", 2),
    (2, "Blue", "Sky Blue", 4),
    (3, "Green", "Mother Earth", 7),
    (4, "Red", "Sunset", 1),
    (5, "Yellow", "Sunrise", 8)
]

cursor.executemany("INSERT INTO material (id_type, colour, name, material_type_id) VALUES (?, ?, ?, ?)", material)

shelves = [
    (1, 935, 13.5),
    (2, 950, 18),
    (3, 1050, 24.5),
    (4, 1025, 22.5),
    (5, 1100, 26)
]

cursor.executemany("INSERT INTO shelf (id_type, humidity_pct, temp_cel) VALUES (?, ?, ?)", shelves)

user_type = [
    (1, "Admin"),
    (2, "Super_Admin")
]

cursor.executemany("INSERT INTO user_type (id_type, name) VALUES (?, ?)", user_type)


users = [
    (1, "james7", "jones7788", "jj7@gmail.com", 2),
    (2, "hugh_55", "pecan7275", "hugh_p55@hotmail.com", 1),
    (3, "scream777", "scary4578", "scream33@hotmail.com", 1),
    (4, "water_123", "Gucci2001", "water7@gmail.com", 2),
    (5, "peter_g7", "griff4508", "peterg@hotmail.com", 2),
    (6, "jake_99", "laugh0910", "jake_p@gmail.com", 1),
]

cursor.executemany("INSERT INTO user (id_type, username, password, email, user_type_id) VALUES (?, ?, ?, ?, ?)", users)

conn.commit()
conn.close()