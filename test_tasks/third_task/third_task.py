"""
3. Объединение данных из разных источников.
Напишите скрипт на Python, который объединяет данные из двух источников.
Первый источник - это CSV-файл с информацией о продуктах (поля: product_id, product_name).
Второй источник - это JSON-файл с данными о продажах (поля: sale_id, product_id, amount).
Скрипт должен объединить данные по product_id и вывести итоговую таблицу
с информацией о продажах для каждого продукта.
"""
import json
import sqlite3

import pandas as pd


class ProductSalesDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY,
                product_id INTEGER,
                amount INTEGER,
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        ''')

    def insert_data_from_csv(self, csv_file):
        products_df = pd.read_csv(csv_file)
        products_df.to_sql('products', self.conn, if_exists='replace',
                           index=False)

    def insert_data_from_json(self, json_file):
        with open(json_file, 'r') as f:
            sales_data = json.load(f)
        sales_df = pd.DataFrame(sales_data)
        sales_df.to_sql('sales', self.conn, if_exists='replace', index=False)

    def query_data(self):
        query = '''
            SELECT p.product_id, p.product_name, s.sale_id, s.amount
            FROM products p
            JOIN sales s ON p.product_id = s.product_id
        '''
        result_df = pd.read_sql_query(query, self.conn)
        return result_df

    def close(self):
        self.conn.close()


def main():
    db = ProductSalesDB('products_sales.db')

    db.create_tables()

    db.insert_data_from_csv('products.csv')
    db.insert_data_from_json('sales.json')

    result_df = db.query_data()
    print(result_df)

    db.close()


if __name__ == "__main__":
    main()
