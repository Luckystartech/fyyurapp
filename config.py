import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
# HOST = os.getenv('DB_HOST', 'localhost:5432')
# USER = os.getenv('DB_USER', 'postgres')
# PASSWORD = os.getenv('DB_PASSWORD', 'Luckystar01')
# NAME = os.getenv('DB_NAME', 'fyyurapp')

# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(USER, PASSWORD, HOST, NAME)
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Luckystar01@localhost:5432/fyyurapp'
SQLALCHEMY_TRACK_MODIFICATIONS = False

