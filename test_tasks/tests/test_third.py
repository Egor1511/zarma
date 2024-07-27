import unittest
import sqlite3
import pandas as pd
import json
import os

from test_tasks.third_task.third_task import ProductSalesDB


class TestProductSalesDB(unittest.TestCase):

    def setUp(self):
        self.db = ProductSalesDB(':memory:')
        self.db.create_tables()

        products_data = [
            (1, 'Product A'),
            (2, 'Product B'),
            (3, 'Product C')
        ]
        products_df = pd.DataFrame(products_data,
                                   columns=['product_id', 'product_name'])
        products_df.to_sql('products', self.db.conn, if_exists='replace',
                           index=False)

        sales_data = [
            {"sale_id": 101, "product_id": 1, "amount": 5},
            {"sale_id": 102, "product_id": 2, "amount": 3},
            {"sale_id": 103, "product_id": 1, "amount": 2},
            {"sale_id": 104, "product_id": 3, "amount": 4}
        ]
        sales_df = pd.DataFrame(sales_data)
        sales_df.to_sql('sales', self.db.conn, if_exists='replace',
                        index=False)

    def tearDown(self):
        self.db.close()

    def test_create_tables(self):
        self.db.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        self.assertIsNotNone(self.db.cursor.fetchone())

        self.db.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='sales'")
        self.assertIsNotNone(self.db.cursor.fetchone())

    def test_insert_data_from_csv(self):
        products_data = [
            (4, 'Product D'),
            (5, 'Product E')
        ]
        products_df = pd.DataFrame(products_data,
                                   columns=['product_id', 'product_name'])
        products_df.to_csv('test_products.csv', index=False)

        self.db.insert_data_from_csv('test_products.csv')

        self.db.cursor.execute(
            'SELECT * FROM products WHERE product_id IN (4, 5)')
        rows = self.db.cursor.fetchall()
        self.assertEqual(len(rows), 2)

        os.remove('test_products.csv')

    def test_insert_data_from_json(self):
        sales_data = [
            {"sale_id": 105, "product_id": 4, "amount": 6},
            {"sale_id": 106, "product_id": 5, "amount": 7}
        ]
        with open('test_sales.json', 'w') as f:
            json.dump(sales_data, f)

        self.db.insert_data_from_json('test_sales.json')

        self.db.cursor.execute(
            'SELECT * FROM sales WHERE sale_id IN (105, 106)')
        rows = self.db.cursor.fetchall()
        self.assertEqual(len(rows), 2)
        os.remove('test_sales.json')

    def test_query_data(self):
        result_df = self.db.query_data()
        result_df = result_df.sort_values(
            by=['product_id', 'sale_id']).reset_index(drop=True)

        expected_data = {
            'product_id': [1, 1, 2, 3],
            'product_name': ['Product A', 'Product A', 'Product B',
                             'Product C'],
            'sale_id': [101, 103, 102, 104],
            'amount': [5, 2, 3, 4]
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df = expected_df.sort_values(
            by=['product_id', 'sale_id']).reset_index(drop=True)

        pd.testing.assert_frame_equal(result_df, expected_df)


if __name__ == '__main__':
    unittest.main()
