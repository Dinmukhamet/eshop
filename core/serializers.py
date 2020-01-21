from rest_framework import serializers
from .models import *


class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brand
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'brand']

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'address', 'comment']

class PurchasedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasedProduct
        fields = ['product', 'name', 'price', 'count', 'total']

class PurchaseSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)
    products = PurchasedProductSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ['date', 'contacts', 'products', 'total_sum']
    
    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        products_data = validated_data.pop('products')
        purchase = Purchase.objects.create(**validated_data)
        for products in products_data:
            product = PurchasedProduct.objects.get_or_create(purchase=purchase, **products)
        for contacts in contacts_data:
            contact = Contact.objects.get_or_create(purchase=purchase, **contacts)
        purchase.save()
        return purchase
