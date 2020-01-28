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


# class SubcategorySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Subcategory
#         fields = ['category', 'parent', 'name']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'brand', 'category', 'total_purchase']


# class SubcategoryToProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = SubcategoryToProduct
#         fields = ['subcategory', 'product']
#         # depth = 1


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'address', 'comment']


class PurchasedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasedProduct
        fields = ['name', 'price', 'count', 'total']


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
        for contacts in contacts_data:
            contact = Contact.objects.get_or_create(
                purchase=purchase, **contacts)
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
        fields = ['products', 'date']

    def create(self, validated_data):
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