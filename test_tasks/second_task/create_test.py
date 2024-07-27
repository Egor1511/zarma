import logging
import sqlite3

logging.basicConfig(
    filename='database_setup.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='w',
    encoding='utf-8'
)

logger = logging.getLogger('DatabaseSetup')


def create_database(database: str) -> None:
    """
    Creates a SQLite database with a 'users' table and inserts some sample data.

    Args:
        database (str): The path to the SQLite database file.
    """
    try:
        logger.info("Connecting to database")
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        logger.info("Creating 'users'")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                UNIQUE(name, age)
            )
        """)

        logger.info("Inserting sample data into 'users' table")
        sample_data = [
            ('name1', 25),
            ('name2', 35),
            ('name3', 32),
            ('name4', 28),
            ('name5', 45)
        ]
        for user in sample_data:
            try:
                cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)",
                               user)
            except sqlite3.IntegrityError:
                logger.info(f"User {user} already exists in the database")

        connection.commit()
        logger.info("Sample data inserted successfully")
    except Exception as e:
        logger.exception("An error occurred while setting up the database")
    finally:
        connection.close()
        logger.info("Database connection closed")


if __name__ == "__main__":
    create_database('users.db')
