from django.shortcuts import render

from .models import *
from .serializers import *
from rest_framework import viewsets
# Create your views here.

class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ContactView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class PurchasedProductView(viewsets.ModelViewSet):
    queryset = PurchasedProduct.objects.all()
    serializer_class = PurchasedProductSerializer

class PurchaseView(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer