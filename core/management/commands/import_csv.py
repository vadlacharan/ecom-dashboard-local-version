import csv
from django.core.management.base import BaseCommand
from core.models import Order
from datetime import datetime

class Command(BaseCommand):
    help = "Import orders data from CSV file after preprocessing"

    def handle(self, *args, **kwargs):
        file_path = 'data/orders.csv'  # Adjust the path to your CSV file
        orders = []

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            i=1
            for row in reader:
                if i<=1:print(row)
                i+=1
                
                
                try:
                    # Preprocess and typecast the data to match the database fields
                    order_date = row['order_date'] # Convert to DateField
                    time = datetime.strptime(row['time'], '%H:%M:%S')  # Convert to TimeField
                    aging = int(row['aging']) if row['aging'] else 0
                    customer_id = row['customer_id']
                    gender = row['gender'].capitalize()  # Normalize case
                    device_type = row['device_type']
                    customer_login_type = row['customer_login_type']
                    product_category = row['product_category']
                    product = row['product']
                    sales = float(row['sales']) if row['sales'] else 0.0
                    quantity = int(row['quantity']) if row['quantity'] else 0
                    discount = float(row['discount']) if row['discount'] else 0.0
                    profit = float(row['profit']) if row['profit'] else 0.0
                    shipping_cost = float(row['shipping_cost']) if row['shipping_cost'] else 0.0
                    order_priority = row['order_priority']
                    payment_method = row['payment_method']

                    # Create Order object
                    order = Order(
                        order_date=order_date,
                        time=time,
                        aging=aging,
                        customer_id=customer_id,
                        gender=gender,
                        device_type=device_type,
                        customer_login_type=customer_login_type,
                        product_category=product_category,
                        product=product,
                        sales=sales,
                        quantity=quantity,
                        discount=discount,
                        profit=profit,
                        shipping_cost=shipping_cost,
                        order_priority=order_priority,
                        payment_method=payment_method
                    )
                    orders.append(order)

                except Exception as e:
                    print(e)
                    continue

        # Bulk create orders in the database
        if orders:
            Order.objects.bulk_create(orders)
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(orders)} records!"))
        else:
            self.stdout.write(self.style.WARNING("No valid records to import!"))
