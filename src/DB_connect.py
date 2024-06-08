import psycopg2
from config import config

class DBManager:
    def __init__(self):
        params = config()
        self.conn = psycopg2.connect(**params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.database_name = 'test'

    def create_database(self):
        """Создание базы данных."""
        # Удаление и создание базы данных
        self.cur.execute(f'DROP DATABASE IF EXISTS {self.database_name}')
        self.cur.execute(f'CREATE DATABASE {self.database_name}')

    def create_tables(self):
        """Создание таблиц в базе данных."""
        create_tables_queries = [
            """
            CREATE TABLE IF NOT EXISTS categories (
                category_id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                path VARCHAR(255)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id SERIAL PRIMARY KEY,
                product_name VARCHAR(100),
                category_id INT,
                unit_price DECIMAL(10, 2),
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id SERIAL PRIMARY KEY,
                first_name VARCHAR(100),
                middle_name VARCHAR(100),
                last_name VARCHAR(100),
                address TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id SERIAL PRIMARY KEY,
                customer_id INT,
                order_date TIMESTAMP,
                total_quantity INT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS order_details (
                order_id INT,
                delivery_address TEXT,
                status VARCHAR(50),
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id SERIAL PRIMARY KEY,
                order_id INT,
                product_id INT,
                quantity INT,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
            """
        ]

        insert_data_queries = [
            """
            INSERT INTO categories (name, path) VALUES 
            ('Электроника', '/1/'),
            ('Телевизоры', '/1/2/'),
            ('Смартфоны', '/1/3/'),
            ('Айфон 15', '/1/3/4/');
            """,
            """
            INSERT INTO products (product_name, category_id, unit_price) VALUES 
            ('Samsung TV', 2, 500.00),
            ('iPhone 15', 4, 1200.00);
            """,
            """
            INSERT INTO customers (first_name, middle_name, last_name, address) VALUES 
            ('Иван', 'Иванович', 'Иванов', 'ул. Пушкина, д. 10');
            """,
            """
            INSERT INTO orders (customer_id, order_date, total_quantity) VALUES 
            (1, '2024-06-07 10:00:00', 2);
            """,
            """
            INSERT INTO order_details (order_id, delivery_address, status) VALUES 
            (1, '123 Main St, Cityville', 'Отправлен');
            """,
            """
            INSERT INTO order_items (order_id, product_id, quantity) VALUES 
            (1, 1, 1),
            (1, 2, 1);
            """
        ]

        with psycopg2.connect(dbname=self.database_name, **config()) as conn:
            with conn.cursor() as cur:
                for query in create_tables_queries:
                    cur.execute(query)
                for query in insert_data_queries:
                    cur.execute(query)

if __name__ == '__main__':
    db_manager = DBManager()
    db_manager.create_database()
    db_manager.create_tables()