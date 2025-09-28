import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Admin connection to create database and user
ADMIN_DB_URL = "postgresql://postgres@localhost:5432/postgres"
DATABASE_NAME = "hangout_db"
USER_NAME = "hangout_user"
USER_PASSWORD = "your_secure_password"  # Replace with a strong password
APP_DB_URL = f"postgresql://{USER_NAME}:{USER_PASSWORD}@localhost:5432/{DATABASE_NAME}"

def create_database_and_user():
    try:
        # Connect to PostgreSQL as admin
        conn = psycopg2.connect(ADMIN_DB_URL)
        conn.set_session(autocommit=True)
        cursor = conn.cursor()

        # Create database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE_NAME)))
        print(f"Database {DATABASE_NAME} created.")

        # Create user and grant privileges
        cursor.execute(
            sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(USER_NAME)),
            [USER_PASSWORD]
        )
        cursor.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                sql.Identifier(DATABASE_NAME), sql.Identifier(USER_NAME)
            )
        )
        print(f"User {USER_NAME} created and granted privileges.")

        cursor.close()
        conn.close()
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database {DATABASE_NAME} already exists.")
    except psycopg2.errors.DuplicateObject:
        print(f"User {USER_NAME} already exists.")
    except Exception as e:
        print(f"Error: {e}")

def create_tables():
    # Use SQLAlchemy to create tables (same as db.py)
    from backend.db import Base, engine
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    create_database_and_user()
    create_tables()