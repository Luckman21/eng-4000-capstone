# A class of constants for the backend.  Classes should refer to this class when using globally defined constants to ensure parity.
import os

# Get the environment variable to determine which DB URL to use
password = 'JanusIsThe_ROMAN_GodOfTransitions44'
address = 'db.lzulfwvbuuoaipbbdzmi.supabase.co'

# Use different database URLs based on the environment
print(f"env var: {os.getenv('ENV')}")
if os.getenv('ENV') == 'production':
    DATABASE_URL = f"postgresql://postgres.lzulfwvbuuoaipbbdzmi:{password}@aws-0-ca-central-1.pooler.supabase.com:5432/postgres"
    DATABASE_URL_TEST = f"postgresql://postgres.lzulfwvbuuoaipbbdzmi:{password}@aws-0-ca-central-1.pooler.supabase.com:5432/postgres"
    DATABASE_URL_ASYNC = f"postgresql+asyncpg://postgres.lzulfwvbuuoaipbbdzmi:{password}@aws-0-ca-central-1.pooler.supabase.com:5432/postgres"
    print("prod")
else:
    DATABASE_URL = "postgresql://postgres:0000@localhost/capstone_db"
    DATABASE_URL_TEST = "postgresql://postgres:0000@localhost/capstone_db"
    DATABASE_URL_ASYNC = "postgresql+asyncpg://postgres:0000@localhost/capstone_db"
    print("dev")
    
# The URL for our database



DATABASE_URL_SQLLITE = 'sqlite:///../../db/capstone_db.db' # PRODUCTION
DATABASE_URL_TEST_SQLLITE = 'sqlite:///nextjs-fastapi/db/capstone_db.db' # TESTING

# LOCAL HOST URLS
LOCALHOST_TEST =  "http://localhost:3000"
DOCKER_TEST = "http://frontend:3000"

THRESHOLD = 50  # 50g mass threshold for materials

HUMIDITY_TOLERANCE = 20.0
TEMPERATURE_TOLERANCE = 30.0

SECRET_KEY = "your-secret-key"

MAILER_EMAIL = 'pantheonprototyping@gmail.com'
