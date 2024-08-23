from django.db import models

# Create your models here.


class Customer(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = ("Customer")
        verbose_name_plural = ("Customers")

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    STATUS = (('', 'Status'), ('pending', 'pending'), ('paid', 'paid'), 
              ('refunded', 'refunded'),)
    PAYMENT_TYPE = (('Cash', 'Cash'), ('Cheque', 'Cheque'),)
    customer = models.ForeignKey(
        Customer, related_name='order_customer', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_product', on_delete=models.CASCADE)
    order_no = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    payment_type = models.CharField(
        max_length=10, choices=PAYMENT_TYPE, default='')
    paid = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    total_amount = models.DecimalField(
        max_digits=19, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_no

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
