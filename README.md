Проект "Управление номенклатурой и заказами"
Описание проекта
Проект представляет собой систему управления номенклатурой товаров, категориями товаров и заказами покупателей. Включает в себя создание базы данных и таблиц с помощью SQL запросов.

Структура базы данных
categories:

category_id SERIAL PRIMARY KEY
name VARCHAR(100)
path VARCHAR(255)
products:

product_id SERIAL PRIMARY KEY
product_name VARCHAR(100)
category_id INT
unit_price DECIMAL(10, 2)
FOREIGN KEY (category_id) REFERENCES categories(category_id)
customers:

customer_id SERIAL PRIMARY KEY
first_name VARCHAR(100)
middle_name VARCHAR(100)
last_name VARCHAR(100)
address TEXT
orders:

order_id SERIAL PRIMARY KEY
customer_id INT
order_date TIMESTAMP
total_quantity INT
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
order_details:

order_id INT
delivery_address TEXT
status VARCHAR(50)
FOREIGN KEY (order_id) REFERENCES orders(order_id)
order_items:

order_item_id SERIAL PRIMARY KEY
order_id INT
product_id INT
quantity INT
FOREIGN KEY (order_id) REFERENCES orders(order_id)
FOREIGN KEY (product_id) REFERENCES products(product_id)
Используемые технологии
Реляционная база данных (PostgreSQL)
SQL
Установка и использование
Выполните SQL запросы для создания таблиц, описанных в разделе "Структура базы данных".
Начните использовать систему управления номенклатурой и заказами.

Получение информации о сумме товаров, заказанных каждым клиентом.
SELECT c.first_name || ' ' || c.middle_name || ' ' || c.last_name AS "Наименование клиента", SUM(p.unit_price * oi.quantity) AS "Сумма"
        FROM customers c 
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY c.first_name, c.middle_name, c.last_name;

Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры.
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

практика метода 
