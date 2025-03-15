# A class of constants for the backend.  Classes should refer to this class when using globally defined constants to ensure parity.

# The URL for our database
DATABASE_URL = "postgresql://postgres:0000@localhost/capstone_db"
DATABASE_URL_TEST = "postgresql://postgres:0000@localhost/capstone_db"
DATABASE_URL_ASYNC = "postgresql+asyncpg://postgres:0000@localhost/capstone_db"

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
