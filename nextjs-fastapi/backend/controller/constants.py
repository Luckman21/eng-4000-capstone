# A class of constants for the backend.  Classes should refer to this class when using globally defined constants to ensure parity.

# The URL for our database
DATABASE_URL = 'sqlite:///../../db/capstone_db.db' # PRODUCTION
DATABASE_URL_TEST = 'sqlite:///nextjs-fastapi/db/capstone_db.db' # TESTING

# LOCAL HOST URLS
LOCALHOST_TEST =  "http://localhost:3000"
DOCKER_TEST = "http://frontend:3000"

THRESHOLD = 50  # 50g mass threshold for materials