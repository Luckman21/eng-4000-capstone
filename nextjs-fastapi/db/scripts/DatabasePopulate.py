import sqlite3


def populate_db():
    # Connecting to the database
    conn = sqlite3.connect('../capstone_db.db')

    # Define some links

    money_4_nothing = "https://www.youtube.com/watch?v=JcqhvPNiJzo"
    google = "https://www.google.com/"
    meditations = "https://www.goodreads.com/book/show/30659.Meditations"

    # Enable foreign key enforcement in SQLite (important)
    conn.execute("PRAGMA foreign_keys = ON;")

    cursor = conn.cursor()

    # Populating the different material types given by Pantheon
    material_type = [
        ("FDM",),
        ("SLA",),
        ("PLA",),
        ("Silk PLA",),
        ("PETG",),
        ("TPU",),
        ("ABS",),
        ("ASA",),
        ("PAHT CF",),
        ("NYLON",)
    ]

    cursor.executemany("INSERT INTO material_types (type_name) VALUES (?)", material_type) # inserting the names into material type class

    # Populating different shelves with different humidity and temperature values
    shelves = [
        (935, 13.5),
        (950, 18),
        (1050, 24.5),
        (1025, 22.5),
        (1100, 26),
        (800, 10),
        (1200, 29),
        (1000, 22),
        (975, 20),
        (850, 11.5)
    ]

    cursor.executemany("INSERT INTO shelfs (humidity_pct, temperature_cel) VALUES (?, ?)",
                       shelves)  # Inserting shelf values into the class

    # Populating the different materials that are connected with each material type
    material = [
        ("Black", google, 500.0, 1, 1),
        ("Blue", money_4_nothing, 17.8, 1, 1),
        ("Green", meditations, 94.5, 2, 2),
        ("Red", google, 72.6, 2, 2),
        ("Yellow", google, 72.6, 3, 3),
        ("White", google, 72.6, 3, 3),
        ("Brown", google, 72.6, 4, 4),
        ("Teal", google, 50.0, 4, 4),
        ("Silver", google, 90.0, 5, 5),
        ("Purple", money_4_nothing, 72.6, 5, 5),
        ("Gray", money_4_nothing, 72.6, 6, 6),
        ("Orange", money_4_nothing, 723.6, 6, 6),
        ("Maroon", money_4_nothing, 100.6, 7, 7),
        ("Aquamarine", money_4_nothing, 724.6, 7, 7),
        ("Lime", meditations, 72.6, 8, 8),
        ("Crimson", meditations, 72.6, 8, 8),
        ("Pink", meditations, 72.6, 9, 9),
        ("Magenta", meditations, 72.6, 9, 9),
        ("Gold", meditations, 72.6, 10, 10),
        ("Black", meditations, 72.6, 10, 10)

    ]

    cursor.executemany("INSERT INTO materials (colour, supplier_link, mass, material_type_id, shelf_id) VALUES (?, ?, ?, ?, ?)", material) # This will insert the material values into the material class

    # Populating with different user types
    user_type = [
        ("Admin",),
        ("Super_Admin",)
    ]

    cursor.executemany("INSERT INTO user_types (type_name) VALUES (?)", user_type) # Inserting the two user types into the user_type class

    # Populating with multiple users
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


populate_db()