"""
1. Подключение к API и получение данных.
 Напишите скрипт на Python, который подключается к API и получает данные.
 Например, используйте публичное API https://jsonplaceholder.typicode.com/posts.
 Сохраните полученные данные в формате JSON в файл.
"""

import json
import logging
from typing import Any

import requests

logging.basicConfig(
    filename='api_client.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='w',
    encoding='utf-8'
)

logger = logging.getLogger('APIClient')


class APIClient:
    def __init__(self, base_url: str) -> None:
        """
        Initialize the APIClient with a base URL.

        Args:
            base_url (str): The base URL of the API.
        """
        self.base_url = base_url

    def fetch_data(self, endpoint: str) -> list[dict[str, Any]]:
        """
        Fetch data from the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to fetch data from.

        Returns:
            list[dict[str, Any]]: The data retrieved from the API.

        Raises:
            Exception: If the API request fails.
        """
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"Sending request to {url}")
        response = requests.get(url)
        if response.status_code == 200:
            logger.info(f"Data successfully retrieved from {url}")
            return response.json()
        else:
            error_message = f"Failed to connect to API: {response.status_code}"
            logger.error(error_message)
            raise Exception(error_message)

    def save_to_file(self, data: list[dict[str, Any]], filename: str) -> None:
        """
        Save the given data to a file in JSON format.

        Args:
            data (list[dict[str, Any]]): The data to save.
            filename (str): The name of the file to save the data to.
        """
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logger.info(f"Data successfully saved to file {filename}")


def main() -> None:
    api_client = APIClient('https://jsonplaceholder.typicode.com')

    try:
        posts = api_client.fetch_data('posts')
        api_client.save_to_file(posts, 'posts.json')
    except Exception as e:
        logger.exception("An error occurred while executing the script")


if __name__ == "__main__":
    main()
