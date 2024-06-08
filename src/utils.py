import psycopg2
from config import config
from src.DB_connect import DBManager


def get_order_sum_per_customer(cur):
    """Получение информации о сумме товаров, заказанных каждым клиентом."""
    query = """
        SELECT c.first_name || ' ' || c.middle_name || ' ' || c.last_name AS "Наименование клиента", SUM(p.unit_price * oi.quantity) AS "Сумма"
        FROM customers c 
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY c.first_name, c.middle_name, c.last_name;
    """
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row[0], "-", row[1])

def count_first_level_child_categories(cur):
    """Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры."""
    query = """
        SELECT 
            parent.name AS "Родительская категория",
            COUNT(child.category_id) AS "Количество дочерних элементов"
        FROM 
            categories parent
        LEFT JOIN 
            categories child ON parent.category_id = CAST(regexp_replace(child.path, '[^0-9]', '', 'g') AS INTEGER)
        WHERE length(child.path) - length(replace(child.path, '/', '')) = 2
        GROUP BY 
            parent.name;
    """
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row[0], "-", row[1])

if __name__ == '__main__':
    db_manager = DBManager()
    # db_manager.create_database()
    # db_manager.create_tables()

    # Подключение к базе данных 'test'
    params = config()
    conn = psycopg2.connect(dbname='test', **params)
    conn.autocommit = True
    cur = conn.cursor()

    # Вызов функций для выполнения задач
    get_order_sum_per_customer(cur)
    count_first_level_child_categories(cur)

    # Закрытие соединения
    cur.close()
    conn.close()