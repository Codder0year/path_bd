from src.DB_connect import DBManager
from src.utils import get_order_sum_per_customer, count_first_level_child_categories
import psycopg2
from config import config

def main():
    # Создание и настройка базы данных
    db_manager = DBManager()
    db_manager.create_database()
    db_manager.create_tables()

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

if __name__ == '__main__':
    main()