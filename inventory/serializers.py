from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['updated_at', 'created_at']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['updated_at', 'created_at']
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['updated_at', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [ 'product', 'quantity']
        
class OrderPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'payment_type']
        
        
class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        exclude = [ 'created_at']
       

class OrderListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    customer = CustomerSerializer()
    class Meta:
        model = Order
        exclude = ['updated_at', ]
