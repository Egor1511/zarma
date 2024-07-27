"""
2. Обработка данных с использованием SQL
 Представьте, что у вас есть таблица users в базе данных SQLite
 с полями id, name, и age. Напишите Python-скрипт,
 который подключается к этой базе данных,
 выбирает всех пользователей старше 30 лет и выводит их имена и возраст.
"""

import logging
import sqlite3

logging.basicConfig(
    filename='query_users.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='w',
    encoding='utf-8'
)

logger = logging.getLogger('QueryUsers')


def get_users_over_age(database: str, age_threshold: int) -> list[
    tuple[str, int]]:
    """
    Connects to the SQLite database and retrieves all users over a specified age.

    Args:
        database (str): The path to the SQLite database file.
        age_threshold (int): The age threshold to filter users.

    Returns:
        list[tuple[str, int]]: A list of tuples containing the names and ages
        of users over the specified age.
    """
    connection = None
    if not isinstance(age_threshold, int):
        raise ValueError("age_threshold must be an integer")
    try:
        logger.info(f"Connecting to database '{database}'")
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        logger.info(f"Querying for users older than {age_threshold}")
        query = "SELECT name, age FROM users WHERE age > ?"
        cursor.execute(query, (age_threshold,))
        results = cursor.fetchall()

        logger.info(
            f"Retrieved {len(results)} users over the age of {age_threshold}")
        return results
    except Exception as e:
        logger.exception("An error occurred while querying the database")
        return []
    finally:
        if connection is not None:
            connection.close()
            logger.info("Database connection closed")


def main() -> None:
    database = 'users.db'
    age_threshold = 30

    users = get_users_over_age(database, age_threshold)
    print(users)
    for name, age in users:
        logger.info(f"Name: {name}, Age: {age}")


if __name__ == "__main__":
    main()
