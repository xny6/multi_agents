from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

vn = MyVanna(config={'model': 'gemma3:27b'})

vn.connect_to_mysql(host='10.4.160.88', dbname='my_database', user='xny_remote', password='ny20050417', port=3306)
# vn.connect_to_mysql(host='10.7.162.54', dbname='my_database', user='xny_remote', password='ny20050417', port=3306)

def train_vn(vn):
    vn.train(ddl='''
    CREATE TABLE brands (
        brand_id INT NOT NULL AUTO_INCREMENT,
        brand_name VARCHAR(100),
        PRIMARY KEY (brand_id)
    );
    ''')

    vn.train(ddl='''
    CREATE TABLE customers (
        customer_id INT NOT NULL AUTO_INCREMENT,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        email VARCHAR(255),
        phone_number VARCHAR(50),
        address TEXT,
        registration_date DATE,
        PRIMARY KEY (customer_id),
        UNIQUE (email)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE orders (
        order_id INT NOT NULL AUTO_INCREMENT,
        customer_id INT,
        order_date DATE,
        total_amount DECIMAL(10,2),
        status VARCHAR(50),
        shipping_address TEXT,
        warranty_status VARCHAR(20),
        manufacturing_batch_id VARCHAR(50),
        PRIMARY KEY (order_id),
        CONSTRAINT orders_ibfk_1 FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE order_items (
        order_item_id INT NOT NULL AUTO_INCREMENT,
        order_id INT,
        product_id INT,
        quantity INT,
        unit_price DECIMAL(10,2),
        PRIMARY KEY (order_item_id),
        CONSTRAINT order_items_ibfk_1 FOREIGN KEY (order_id) REFERENCES orders(order_id),
        CONSTRAINT order_items_ibfk_2 FOREIGN KEY (product_id) REFERENCES products(product_id)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE products (
        product_id INT NOT NULL AUTO_INCREMENT,
        product_name VARCHAR(255),
        price DECIMAL(10,2),
        stock_quantity INT,
        category VARCHAR(100),
        brand_id INT,
        release_date DATE,
        is_active TINYINT(1),
        PRIMARY KEY (product_id),
        CONSTRAINT products_ibfk_1 FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE product_feature (
        feature_id INT NOT NULL AUTO_INCREMENT,
        product_id INT,
        question TEXT,
        feature TEXT,
        PRIMARY KEY (feature_id),
        CONSTRAINT product_feature_ibfk_1 FOREIGN KEY (product_id) REFERENCES products(product_id)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE product_reviews (
        id INT NOT NULL AUTO_INCREMENT,
        review_id INT,
        product_id INT,
        customer_id INT,
        rating INT,
        comment VARCHAR(255),
        review_date VARCHAR(255),
        is_approved VARCHAR(255),
        PRIMARY KEY (id)
        -- 未定义外键，如需要可添加：
        -- FOREIGN KEY (product_id) REFERENCES products(product_id),
        -- FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE purchase_orders (
        purchase_order_id INT NOT NULL AUTO_INCREMENT,
        supplier_id INT,
        order_date DATE,
        expected_delivery_date DATE,
        total_cost DECIMAL(10,2),
        PRIMARY KEY (purchase_order_id),
        CONSTRAINT purchase_orders_ibfk_1 FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    );
    ''')

    vn.train(ddl='''
    CREATE TABLE returns (
        return_id INT NOT NULL AUTO_INCREMENT,
        order_id INT,
        product_id INT,
        return_reason VARCHAR(255),
        return_date DATE,
        refund_amount DECIMAL(10,2),
        status VARCHAR(50),
        PRIMARY KEY (return_id),
        CONSTRAINT returns_ibfk_1 FOREIGN KEY (order_id) REFERENCES orders(order_id),
        CONSTRAINT returns_ibfk_2 FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    ''')

    vn.train(ddl='''
    CREATE TABLE suppliers (
        supplier_id INT NOT NULL AUTO_INCREMENT,
        supplier_name VARCHAR(255),
        contact_person VARCHAR(255),
        phone VARCHAR(20),
        supplied_product_type VARCHAR(50),
        PRIMARY KEY (supplier_id)
    );
    ''')

    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN in_ear_detection INT;''')

    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN wireless_charging INT;''')

    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN wireless_charging INT;''')

    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN fast_charging INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN eSIM INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN WiFi_6 INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN fingerprint_unlock INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN face_unlock INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN Dual_4G INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN Dual_SIM INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN has_3_5mm_headphone_jack INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN NFC INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN blueteeth_calls INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN IP_68 INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN auto_brightness INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN women_health INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN LE_audio INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN Microsoft_swift_pair INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN Google_fast_pair INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN custom_EQ_settings INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN ANC INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN Dual_connection INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN in_ear_detection INT;''')


def train2(vn):
    vn.train(question='Get purchase date, products and warranty status for David Beltran\'s order',sql='''SELECT `orders`.`order_date`, `products`.`product_name`, `warranty_status`
    FROM orders
    JOIN customers ON orders.customer_id = customers.customer_id
    JOIN order_items ON orders.order_id = order_items.order_id
    JOIN products ON order_items.product_id = products.product_id
    WHERE customers.first_name = 'David' AND customers.last_name = 'Beltran'
    ''')

    vn.train(question='Get purchase date, products, price and warranty status for David Beltran\'s order, check them in products, orders, order_items and customers tables.'
    ,sql='''
        SELECT `orders`.`order_date`, `products`.`product_name`, `products`.`price`, `orders`.`warranty_status`
        FROM `customers`
        JOIN `orders` ON `customers`.`customer_id` = `orders`.`customer_id`
        JOIN `order_items` ON `orders`.`order_id` = `order_items`.`order_id`
        JOIN `products` ON `order_items`.`product_id` = `products`.`product_id`
        WHERE `customers`.`first_name` = 'David' AND `customers`.`last_name` = 'Beltran'


    ''')

    vn.train(question='I am Kim Osborne. I bought a earphone from your company a few months ago. How does the Dual Connection feature work?',sql=
    '''
        SELECT `orders`.`order_date`, `products`.`product_name`, `products`.`price`, `orders`.`warranty_status`
        FROM `customers`
        JOIN `orders` ON `customers`.`customer_id` = `orders`.`customer_id`
        JOIN `order_items` ON `orders`.`order_id` = `order_items`.`order_id`
        JOIN `products` ON `order_items`.`product_id` = `products`.`product_id`
        WHERE `customers`.`first_name` = 'Kim' AND `customers`.`last_name` = 'Osborne'

    ''')

def train3(vn):
    vn.train(question='Get and price of Ear (a), CMF Buds Pro 2, Buds Pro earbuds, Ear (stick), Nothing Ear Stick earbuds, CMF Buds 2, Ear (1) earbuds, or other devices with similar names.',
        sql=r"""SELECT `products`.`product_name`, `products`.`price`
            FROM products
            WHERE `product_name` IN ('Ear (a)', 'CMF Buds Pro 2', 'Buds Pro earbuds', 'Ear (stick)', 'Nothing Ear Stick earbuds', 'CMF Buds 2', 'Ear (1) earbuds')
            OR `product_name` LIKE '%Ear%' OR `product_name` LIKE '%Buds%'
            ORDER BY `product_name` ASC

        """)
    
    vn.train(question='Get the price of Nothing Ear 2, CMF Buds Pro 2, Ear (stick), Buds Pro Earbuds, Nothing Ear (a), and Ear (a), or other earphones with similar names that support Active Noise Cancellation.',
        sql=r"""SELECT `products`.`product_name`, `products`.`price`
                FROM products
                WHERE `product_name` IN ('Ear (a)', 'CMF Buds Pro 2', 'Buds Pro earbuds', 'Ear (stick)', 'Nothing Ear Stick earbuds', 'CMF Buds 2', 'Ear (1) earbuds')
                OR `product_name` LIKE '%Ear%' OR `product_name` LIKE '%Buds%'
                ORDER BY `product_name` ASC

            """
    )

    vn.train(question='Get the name and price of the devices which support NFC',
        sql="""SELECT `products`.`product_name`, `products`.`price`
                FROM products
                WHERE `products`.`NFC` = 1
            """
    )

    vn.train(question='Get the name and price of the devices which support NFC',
        sql="""SELECT `products`.`product_name`, `products`.`price`
                FROM products
                WHERE `products`.`NFC` = 1
            """
    )
    vn.train(question='Get the name and weight of CMF Buds Pro 2, Nothing Ear Stick, Buds Pro Earbuds, CMF Buds (2), Earstick, or other devices with similar name.',
        sql=r'''SELECT `products`.`product_name`, `products`.`weight`
                FROM products
                WHERE `product_name` LIKE '%Nothing Ear%' OR `product_name` = 'Nothing Ear 2' OR `product_name` LIKE '%Buds%' OR `product_name` LIKE '%stick%'
        ''')
    
    vn.train(question='Get the number of purchases for Nothing Ear (a), CMF Buds Pro 2, Ear (open), Ear Stick, Ear (1), Ear (2) or other devices with similar names.',
        sql=r'''SELECT 
                    products.product_name,
                    COUNT(DISTINCT order_items.order_id) AS num_purchases
                FROM 
                    order_items
                JOIN 
                    products ON order_items.product_id = products.product_id
                WHERE 
                    products.product_name LIKE '%Nothing Ear (%)' 
                    OR products.product_name LIKE '%CMF Buds Pro%' 
                    OR products.product_name LIKE '%Ear (open)%' 
                    OR products.product_name LIKE '%Ear Stick%' 
                    OR products.product_name LIKE '%Ear (1)%' 
                    OR products.product_name LIKE '%Ear (2)%'
                GROUP BY 
                    products.product_id, products.product_name
                ORDER BY 
                    num_purchases DESC
        ''')

    vn.train(question='Get the name and corresponding rating of Nothing Ear (a), CMF Buds Pro 2, Ear (open), Ear Stick, Ear (1), Ear (2) or other devices with similar names.',
        sql=r'''SELECT `product_reviews`.`review_id`, `product_reviews`.`rating`, `products`.`product_name`
                FROM `product_reviews`
                JOIN `products` ON (`product_reviews`.`product_id` = `products`.`product_id`)
                WHERE `product_reviews`.`product_id` IN (
                    SELECT `product_id` FROM `products` WHERE `product_name` LIKE '%Nothing Ear (a)%' 
                    OR `product_name` = 'CMF Buds Pro 2' 
                    OR `product_name` LIKE '%Ear (open)%'
                    OR `product_name` LIKE '%Ear Stick%'
                    OR `product_name` LIKE '%Ear (1)%'
                    OR `product_name` LIKE '%Ear (2)%') 

                ORDER BY `review_id`
        ''')


import pandas as pd


# def save_dataframe_to_json(df, filename):
#     # ✅ 这些字段即使是字符串也不要尝试转为日期
#     blacklist_columns = ['weight', 'price', 'stock_quantity', 'total_amount', 'quantity', 'refund_amount']

#     for col in df.columns:
#         if col in blacklist_columns:
#             continue  # ❗跳过黑名单字段

#         # 如果是 datetime 类型，直接格式化
#         if pd.api.types.is_datetime64_any_dtype(df[col]):
#             df[col] = df[col].dt.strftime('%Y-%m-%d')

#         # 如果是 object 类型，尝试解析日期字符串
#         elif df[col].dtype == object:
#             try:
#                 parsed = pd.to_datetime(df[col], errors='raise', format='%Y-%m-%d')
#                 df[col] = parsed.dt.strftime('%Y-%m-%d')
#             except Exception:
#                 continue  # 不是日期字符串就跳过

#     # ✅ 保存为 JSON 文件
#     df.to_json(filename, orient='records', force_ascii=False, indent=4)







def run_sql_query(my_vn=vn, question=''):
    """
    执行 SQL 查询并返回结果
    """
    sql = my_vn.generate_sql(question=question, allow_llm_to_see_data=True)
    print('===============================================')
    print(f'sql: {sql}')
    answer = my_vn.run_sql(sql)
    print('===============================================')
    print(f'answer: {answer}')
    # print(answer.dtypes)

    # ✅ 这些字段即使是字符串也不要尝试转为日期
    blacklist_columns = ['weight', 'price', 'stock_quantity', 'total_amount', 'quantity', 'refund_amount']

    for col in answer.columns:
        if col in blacklist_columns:
            continue  # ❗跳过黑名单字段

        # 如果是 datetime 类型，直接格式化
        if pd.api.types.is_datetime64_any_dtype(answer[col]):
            answer[col] = answer[col].dt.strftime('%Y-%m-%d')

        # 如果是 object 类型，尝试解析日期字符串
        elif answer[col].dtype == object:
            try:
                parsed = pd.to_datetime(answer[col], errors='raise', format='%Y-%m-%d')
                answer[col] = parsed.dt.strftime('%Y-%m-%d')
            except Exception:
                continue  # 不是日期字符串就跳过

    # ✅ 转换为 JSON 字符串
    json_data = answer.to_json(orient='records', force_ascii=False, indent=4)
    
    return json_data



train_vn(vn)
train2(vn)
train3(vn)
print(run_sql_query(vn, question='Get the product name in return form where return date is 2025-05-12'))

# vn.ask(question=question, allow_llm_to_see_data=True,visualize=False)
# from vanna.flask import VannaFlaskApp
# app = VannaFlaskApp(vn)
# app.run()








