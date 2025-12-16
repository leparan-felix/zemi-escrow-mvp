from django.db import models
import hashlib, random, string

def hash_phone(phone):
    return hashlib.sha256(phone.encode()).hexdigest()

def generate_delivery_code():
    return ''.join(random.choices(string.digits, k=6))

class Order(models.Model):
    order_reference = models.CharField(max_length=20, unique=True)
    phone_hashed = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField()
    delivery_code = models.CharField(max_length=6)
    status = models.CharField(max_length=20, default='awaiting_payment')
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
