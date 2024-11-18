from django.db import models

# Create your models here.

class Order(models.Model):
    order_date = models.DateField()
    time = models.TimeField()
    aging = models.IntegerField()
    customer_id = models.IntegerField()
    gender = models.CharField(max_length=10)
    device_type = models.CharField(max_length=20)
    customer_login_type = models.CharField(max_length=20)
    product_category = models.CharField(max_length=50)
    product = models.CharField(max_length=50)
    sales = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=5, decimal_places=2)
    order_priority = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=20)

    def __str__(self):
        return f"Order {self.id}"
