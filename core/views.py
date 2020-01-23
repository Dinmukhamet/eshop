from django.shortcuts import render

from .models import *
from .serializers import *
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class SubcategoryView(viewsets.ModelViewSet):
#     queryset = Subcategory.objects.all()
#     serializer_class = SubcategorySerializer


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

# class SubcategoryToProductView(viewsets.ModelViewSet):
#     queryset = SubcategoryToProduct.objects.all()
#     serializer_class = SubcategoryToProductSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['subcategory']


class ContactView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class PurchasedProductView(viewsets.ModelViewSet):
    queryset = PurchasedProduct.objects.all()
    serializer_class = PurchasedProductSerializer


class PurchaseView(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentRatingView(viewsets.ModelViewSet):
    queryset = CommentRating.objects.all()
    serializer_class = CommentRatingSerializer