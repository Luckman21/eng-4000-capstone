
import psycopg # type: ignore
from argon2 import PasswordHasher

def populate_db():
    # PostgreSQL connection string (update password and database name if needed)
    DATABASE_URL = "postgresql://postgres:0000@localhost/capstone_db"

    # Connect to the PostgreSQL database
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Define some links
    amazon_sale = 'https://www.amazon.ca/ELEGOO-Filament-Dimensional-Accuracy-Compatible/dp/B0BM95MYNX/ref' \
                  '=sxin_15_pa_sp_search_thematic_sspa?content-id=amzn1.sym.46621be6-fabe-4126-8501-d32c96c42a24' \
                  '%3Aamzn1.sym.46621be6-fabe-4126-8501-d32c96c42a24&cv_ct_cx=PLA&keywords=PLA&pd_rd_i=B0BM95MYNX' \
                  '&pd_rd_r=801386cf-36e0-470c-aa3d-fd4084381423&pd_rd_w=usjfA&pd_rd_wg=A4vii&pf_rd_p=46621be6-fabe' \
                  '-4126-8501-d32c96c42a24&pf_rd_r=TQBGZJC1XMJR5CW8WMAX&qid=1739823127&sbo=RZvfv%2F%2FHxDF' \
                  '%2BO5021pAnSA%3D%3D&sr=1-1-acb80629-ce74-4cc5-9423-11e8801573fb-spons&sp_csd' \
                  '=d2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM&th=1 '
    digitmaker_sale = 'https://www.digitmakers.ca/collections/esun-filaments/products/esun-emarble-pla-filament-1-75mm-1kg'
    table_sale = 'https://www.digitmakers.ca/collections/offer-of-the-week-3d-printing-canada-3d-filaments-canada/products/d3d-premium-petg-filament-1-75-mm-1kg-spool?variant=8112650649636'

    non_sale_item = 'https://www.digitmakers.ca/collections/esun-filaments/products/esun-etpu-95a-filament-1-75mm-1kg-various-colors?variant=33750608445571'
    # Populate material types
    material_type = [
        ("PLA",),
        ("TPU",),
        ("PETG",),
    ]
    cursor.executemany("INSERT INTO material_types (type_name) VALUES (%s) ON CONFLICT (type_name) DO NOTHING", material_type)

    # Populate shelves
    shelves = [
        (935, 13.5),
    ]
    cursor.executemany("INSERT INTO shelfs (humidity_pct, temperature_cel) VALUES (%s, %s)", shelves)

    # Populate materials
    material = [
        ("Black", amazon_sale, 500.0, 1, 1),
        ("Marble", digitmaker_sale, 17.8, 1, 1),
        ("White", non_sale_item, 200.0, 2, 1),
        ("Black", table_sale, 200.0, 3, 1)

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
        ("Luca", ph.hash("0000"), "lucafili@my.yorku.ca", 2),
        ("Other Luca", ph.hash("pecan7275"), "lfilippelli5@gmail.com", 1),
    ]

    cursor.executemany("INSERT INTO users (username, password, email, user_type_id) VALUES (%s, %s, %s, %s) ON CONFLICT (username) DO NOTHING", users)

    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()

populate_db()
