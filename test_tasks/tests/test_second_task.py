import unittest
import sqlite3
import os

from test_tasks.second_task.create_test import create_database
from test_tasks.second_task.second_task import get_users_over_age


class TestGetUsersOverAge(unittest.TestCase):
    def setUp(self):
        self.database = 'test_users.db'
        if os.path.exists(self.database):
            os.remove(self.database)
        create_database(self.database)

    def tearDown(self):
        if os.path.exists(self.database):
            os.remove(self.database)

    def test_get_users_over_age(self):
        users = get_users_over_age(self.database, 30)
        expected_users = [
            ('name2', 35),
            ('name3', 32),
            ('name5', 45)
        ]
        self.assertEqual(users, expected_users)

    def test_get_users_over_age_no_results(self):
        users = get_users_over_age(self.database, 50)
        expected_users = []
        self.assertEqual(users, expected_users)

    def test_get_users_over_age_invalid_age(self):
        with self.assertRaises(ValueError):
            get_users_over_age(self.database, 'invalid_age')

if __name__ == '__main__':
    unittest.main()
