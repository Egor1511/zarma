import os
import sqlite3
import unittest

from test_tasks.second_task.create_test import create_database


class TestCreateDatabase(unittest.TestCase):
    def setUp(self):
        self.database = 'test_users.db'
        if os.path.exists(self.database):
            os.remove(self.database)

    def tearDown(self):
        if os.path.exists(self.database):
            os.remove(self.database)

    def test_create_database(self):
        create_database(self.database)

        self.assertTrue(os.path.exists(self.database))

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("SELECT name, age FROM users")
        users = cursor.fetchall()
        connection.close()

        expected_users = [
            ('name1', 25),
            ('name2', 35),
            ('name3', 32),
            ('name4', 28),
            ('name5', 45)
        ]
        self.assertEqual(users, expected_users)


if __name__ == '__main__':
    unittest.main()
