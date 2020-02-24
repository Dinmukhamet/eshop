from rest_framework import serializers
from .models import *


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


# PurchasedProduct.objects.values('product').annotate(number_of_purchases = Sum('count')).order_by('-number_of_purchases')


class CustomerInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerInfo
        fields = ['id', 'name', 'email', 'phone_number', 'address', 'comment']


class PurchasedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasedProduct
        fields = ['id', 'product', 'name', 'price',
                  'count', 'sale_value', 'total', 'created_at']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image',
                  'brand', 'category', 'price', 'created_at',
                  'total_purchase']

# class PriceSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Price
#         fields = ['id', 'product', 'price', 'created_at', 'date_to']


class PurchaseSerializer(serializers.ModelSerializer):
    contacts = CustomerInfoSerializer(many=True)
    products = PurchasedProductSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ['id', 'contacts', 'products', 'total_sum', ]

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        products_data = validated_data.pop('products')
        # if products_data is not None:
        purchase = Purchase.objects.create(**validated_data)
        for products in products_data:
            product = PurchasedProduct.objects.get_or_create(
                purchase=purchase, **products)
            # hit = Hit.objects.get_or_create(product=products_data['product'])
        for contacts in contacts_data:
            contact = CustomerInfo.objects.get_or_create(
                purchase=purchase, **contacts)
        # PurchasedProduct.objects.get(purchase=purchase).count
        purchase.save()
        return purchase


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['id', 'product', 'rate', 'created_at']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'product', 'comment', 'created_at']


class CommentRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentRating
        fields = ['id', 'comment', 'rate', 'created_at']


class SliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slider
        fields = ['id', 'image', 'product']


# class ProductToRecommendedProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductToRecommendedProduct
#         fields = ['id', 'recommended_product', 'product']


class RecommendedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecommendedProduct
        fields = ['id', 'date_from', 'date_to', 'category', 'product']

    # def create(self, validated_data):
    #     products_data = validated_data.pop('products')
    #     recommended_product = RecommendedProduct.objects.create(
    #         **validated_data)
    #     for products in products_data:
    #         product = ProductToRecommendedProduct.objects.create(
    #             recommended_product=recommended_product, **products)
    #     recommended_product.save()
    #     return recommended_product


class ProductToSaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductToSale
        fields = ['sale', 'product', 'new_price', 'old_price']


class SaleSerializer(serializers.ModelSerializer):
    products = ProductToSaleSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'date_from', 'date_to', 'value', 'products', 'created']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        sale = Sale.objects.create(**validated_data)
        for products in products_data:
            product = ProductToSale.objects.create(sale=sale, **products)
        sale.save()
        return sale
