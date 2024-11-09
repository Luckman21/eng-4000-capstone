import sqlite3


def populate_db():
    # Connecting to the database
    conn = sqlite3.connect('../capstone_db.db')

    # Enable foreign key enforcement in SQLite (important)
    conn.execute("PRAGMA foreign_keys = ON;")

    cursor = conn.cursor()

    try:
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

        cursor.executemany("INSERT INTO material_types (type_name) VALUES (?)",
                           material_type)  # Inserting into material_types

        # Populating the different materials connected with each material type
        material = [
            ("Black", "Smokey Black", 500.0, 1),
            ("Blue", "Sky Blue", 17.8, 1),
            ("Green", "Mother Earth", 94.5, 2),
            ("Red", "Sunset", 72.6, 2),
            ("Yellow", "Sunrise", 72.6, 3),
            ("White", "Surface Moon", 72.6, 3),
            ("Brown", "Dirt Ground", 72.6, 4),
            ("Teal", "Seaweed", 50.0, 4),
            ("Silver", "Starry Night", 90.0, 5),
            ("Purple", "Barney", 72.6, 5),
            ("Gray", "Cloudy Day", 72.6, 6),
            ("Orange", "Pumpkin", 723.6, 6),
            ("Maroon", "Oakwood", 100.6, 7),
            ("Aquamarine", "Poolside", 724.6, 7),
            ("Lime", "Sprite", 72.6, 8),
            ("Crimson", "Lobster", 72.6, 8),
            ("Pink", "Barbie", 72.6, 9),
            ("Magenta", "Uniqua", 72.6, 9),
            ("Gold", "Olympics", 72.6, 10),
            ("Black", "Night Sky", 72.6, 10)
        ]

        cursor.executemany("INSERT INTO materials (colour, name, mass, material_type_id) VALUES (?, ?, ?, ?)",
                           material)  # Inserting into materials

        # Populating different shelves with humidity and temperature values
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
                           shelves)  # Inserting into shelfs

        # Populating with different user types
        user_type = [
            ("Admin",),
            ("Super_Admin",)
        ]

        cursor.executemany("INSERT INTO user_types (type_name) VALUES (?)", user_type)  # Inserting into user_types

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

        cursor.executemany("INSERT INTO users (username, password, email, user_type_id) VALUES (?, ?, ?, ?)",
                           users)  # Inserting into users

        # Commit the changes
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
        conn.rollback()  # Rollback if there's an error

    finally:
        conn.close()


# Call the populate_db function to populate the database
populate_db()
