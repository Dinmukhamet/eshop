from django.shortcuts import render
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

# Create your views here.


class BrandView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class SubcategoryView(viewsets.ModelViewSet):
#     queryset = Subcategory.objects.all()
#     serializer_class = SubcategorySerializer


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
# class SubcategoryToProductView(viewsets.ModelViewSet):
#     queryset = SubcategoryToProduct.objects.all()
#     serializer_class = SubcategoryToProductSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['subcategory']


class ContactView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class PurchasedProductView(generics.ListCreateAPIView):
    queryset = PurchasedProduct.objects.all()
    serializer_class = PurchasedProductSerializer

class PurchaseView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

class PurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

class RatingView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentRatingView(generics.ListCreateAPIView):
    queryset = CommentRating.objects.all()
    serializer_class = CommentRatingSerializer

class FavouriteView(generics.ListCreateAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

class FavouriteProductView(generics.ListCreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer

class SliderView(generics.ListAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer