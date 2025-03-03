
import psycopg # type: ignore
from argon2 import PasswordHasher

def populate_db():
    # PostgreSQL connection string (update password and database name if needed)
    DATABASE_URL = "postgresql://postgres:0000@localhost/capstone_db"

    # Connect to the PostgreSQL database
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Define some links
    money_4_nothing = "https://www.youtube.com/watch?v=JcqhvPNiJzo"
    google = "https://www.google.com/"
    meditations = "https://www.goodreads.com/book/show/30659.Meditations"

    # Populate material types
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
    cursor.executemany("INSERT INTO material_types (type_name) VALUES (%s) ON CONFLICT (type_name) DO NOTHING", material_type)

    # Populate shelves
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
    cursor.executemany("INSERT INTO shelfs (humidity_pct, temperature_cel) VALUES (%s, %s)", shelves)

    # Populate materials
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
    cursor.executemany("INSERT INTO materials (colour, supplier_link, mass, material_type_id, shelf_id) VALUES (%s, %s, %s, %s, %s)", material)

    # Populate user types
    user_type = [
        ("Admin",),
        ("Super_Admin",)
    ]
    cursor.executemany("INSERT INTO user_types (type_name) VALUES (%s) ON CONFLICT (type_name) DO NOTHING", user_type)

    # Hash passwords
    ph = PasswordHasher()
    users = [
        ("james7", ph.hash("jones7788"), "jj7@gmail.com", 2),
        ("hugh_55", ph.hash("pecan7275"), "hugh_p55@hotmail.com", 1),
        ("scream777", ph.hash("scary4578"), "scream33@hotmail.com", 1),
        ("water_123", ph.hash("Gucci2001"), "water7@gmail.com", 2),
        ("peter_g7", ph.hash("griff4508"), "peterg@hotmail.com", 2),
        ("jake_99", ph.hash("laugh0910"), "jake_p@gmail.com", 1),
        ("josh_z", ph.hash("sides2525"), "josh_23@gmail.com", 2),
        ("simonM", ph.hash("bball0710"), "simon_M@hotmail.com", 1),
        ("Tyler23", ph.hash("Igors1998"), "TytheC@gmail.com", 2),
        ("Drizzy6", ph.hash("Drake2334"), "Drake23@hotmail.com", 1)
    ]

    cursor.executemany("INSERT INTO users (username, password, email, user_type_id) VALUES (%s, %s, %s, %s) ON CONFLICT (username) DO NOTHING", users)


    warnings = [
        ("title 1", "some warning"),
        ("title 2", "some warning 2")
    ]

    cursor.executemany("INSERT INTO warnings (title, description) VALUES (%s, %s)", warnings)

    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()

populate_db()
