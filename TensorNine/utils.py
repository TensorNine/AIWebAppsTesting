# TensorNine/utils.py
import random
import datetime

def generate_random_sales_data(num_records=5):
    products = ['Product A', 'Product B', 'Product C', 'Product D']
    sales_data = []
    for _ in range(num_records):
        sale_date = (datetime.date.today() - datetime.timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
        product_name = random.choice(products)
        quantity = random.randint(1, 10)
        price = round(random.uniform(10.00, 100.00), 2)
        sales_data.append((sale_date, product_name, quantity, price))
    return sales_data

def generate_random_inventory_data(num_records=3):
    items = ['Item X', 'Item Y', 'Item Z', 'Item W']
    inventory_data = []
    for _ in range(num_records):
        item_name = random.choice(items)
        quantity = random.randint(1, 100)
        reorder_level = random.randint(10, 30)
        unit_price = round(random.uniform(5.00, 50.00), 2)
        inventory_data.append((item_name, quantity, reorder_level, unit_price))
    return inventory_data
