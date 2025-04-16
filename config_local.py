import os

# Determine the base directory (i.e., the directory where this script resides)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set the data directory relative to the base directory
DATA_DIR = os.path.join(BASE_DIR, 'pgadmin')

# Run pgAdmin in desktop mode
SERVER_MODE = False

# Optional: Define other paths relative to DATA_DIR
LOG_FILE = os.path.join(DATA_DIR, 'pgadmin4.log')
SQLITE_PATH = os.path.join(DATA_DIR, 'pgadmin4.db')
SESSION_DB_PATH = os.path.join(DATA_DIR, 'sessions')
STORAGE_DIR = os.path.join(DATA_DIR, 'storage')