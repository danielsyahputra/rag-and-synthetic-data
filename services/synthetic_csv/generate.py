import argparse
import random

import pandas as pd
from faker import Faker


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate synthetic e-commerce dataset"
    )
    parser.add_argument(
        "--num-rows", type=int, default=5000, help="Number of rows to generate"
    )
    parser.add_argument(
        "--output", type=str, default="synthetic_dataset.csv", help="Output file path"
    )
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    return parser.parse_args()


def generate_data(num_rows, seed=None):
    if seed:
        random.seed(seed)
        fake = Faker()
        Faker.seed(seed)
    else:
        fake = Faker()

    products = ["Smartphone", "Laptop Case", "Wireless Headphones", "Portable Charger"]
    payment_methods = ["Credit Card", "PayPal", "Debit Card"]
    membership_statuses = ["Gold", "Silver", "Bronze"]
    shipping_methods = ["Express", "Standard"]

    data = []
    for _ in range(num_rows):
        amount_spent = round(random.uniform(20, 500), 2)
        number_of_orders = fake.random_int(min=1, max=50)

        data.append(
            [
                fake.random_int(min=1000, max=9999),
                fake.name(),
                fake.email(),
                random.choice(products),
                fake.date_between(start_date="-30d", end_date="today"),
                amount_spent,
                fake.random_int(min=18, max=80),
                fake.city(),
                random.choice(payment_methods),
                fake.date_between(start_date="-180d", end_date="today"),
                random.choice(membership_statuses),
                number_of_orders,
                round(amount_spent / number_of_orders, 2),
                random.choice(shipping_methods),
                fake.date_time_between(start_date="-2y", end_date="-1y"),
            ]
        )

    return pd.DataFrame(
        data,
        columns=[
            "Customer ID",
            "Name",
            "Email",
            "Product Purchased",
            "Purchase Date",
            "Amount Spent ($)",
            "Age",
            "City",
            "Payment Method",
            "Last Login Date",
            "Membership Status",
            "Number of Orders",
            "Average Order Value ($)",
            "Preferred Shipping Method",
            "Account Created Date",
        ],
    )


def main():
    args = parse_args()
    df = generate_data(args.num_rows, args.seed)
    df.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
