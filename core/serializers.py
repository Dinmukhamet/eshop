from rest_framework import serializers
from .models import *


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'parent']


# PurchasedProduct.objects.values('product').annotate(number_of_purchases = Sum('count')).order_by('-number_of_purchases')


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'address', 'comment']


class PurchasedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasedProduct
        fields = ['product', 'name', 'price', 'count', 'sale_value', 'total']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['get_id', 'name', 'description', 'image',
                  'brand', 'category', 'current_price', 'created_at']
    
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ['product', 'price', 'created_at', 'date_to']

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
            product = PurchasedProduct.objects.get_or_create(
                purchase=purchase, **products)
            # hit = Hit.objects.get_or_create(product=products_data['product'])
        for contacts in contacts_data:
            contact = Contact.objects.get_or_create(
                purchase=purchase, **contacts)
        # PurchasedProduct.objects.get(purchase=purchase).count
        purchase.save()
        return purchase


class FavouriteProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavouriteProduct
        fields = ['favourite', 'product']


class FavouriteSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)
    products = PurchasedProductSerializer(many=True)

    class Meta:
        model = Favourite
        fields = ['contacts', 'products', 'date']

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        products_data = validated_data.pop('products')
        favourite = Favourite.objects.create(**validated_data)
        for products in products_data:
            product = FavouriteProduct.objects.get_or_create(
                favourite=favourite, **products)
        for contacts in contacts_data:
            contact = Contact.objects.get_or_create(
                favourite=favourite, **contacts)
        favourite.save()
        return favourite


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['product', 'rate']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['product', 'comment']


class CommentRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentRating
        fields = ['comment', 'rate']


class SliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slider
        fields = ['image', 'product']


class RecommendedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecommendedProduct
        fields = ['date_from', 'date_to', 'products']


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = ['date_from', 'date_to', 'value', 'products']