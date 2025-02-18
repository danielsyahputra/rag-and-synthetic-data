import random
import pandas as pd
from faker import Faker
from datetime import datetime

fake = Faker()

num_rows = 5000

data = []

for _ in range(num_rows):
    customer_id = fake.random_int(min=1000, max=9999)
    name = fake.name()
    email = fake.email()
    product_purchased = random.choice(["Smartphone", "Laptop Case", "Wireless Headphones", "Portable Charger"])
    purchase_date = fake.date_between(start_date='-30d', end_date='today')
    amount_spent = round(random.uniform(20, 500), 2)
    age = fake.random_int(min=18, max=80)
    city = fake.city()
    payment_method = random.choice(["Credit Card", "PayPal", "Debit Card"])
    last_login_date = fake.date_between(start_date='-180d', end_date='today')
    membership_status = random.choice(["Gold", "Silver", "Bronze"])
    number_of_orders = fake.random_int(min=1, max=50)
    average_order_value = round(amount_spent / number_of_orders, 2)
    preferred_shipping_method = random.choice(["Express", "Standard"])
    account_created_date = fake.date_time_between(start_date='-2y', end_date='-1y')
    
    data.append([customer_id, name, email, product_purchased, purchase_date, amount_spent, age, city, payment_method,
                 last_login_date, membership_status, number_of_orders, average_order_value, preferred_shipping_method,
                 account_created_date])

df = pd.DataFrame(data, columns=['Customer ID', 'Name', 'Email', 'Product Purchased', 'Purchase Date', 
                                 'Amount Spent ($)', 'Age', 'City', 'Payment Method', 'Last Login Date', 
                                 'Membership Status', 'Number of Orders', 'Average Order Value ($)', 
                                 'Preferred Shipping Method', 'Account Created Date'])

df.to_csv('synthetic_dataset.csv', index=False)