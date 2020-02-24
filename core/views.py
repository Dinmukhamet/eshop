from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView, Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Max
# from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import *

# Create your views here.


class BrandView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class ProductHitView(generics.ListAPIView):
    queryset = Product.objects.order_by('-total_purchase')
    serializer_class = ProductSerializer


class ProductDateView(generics.ListAPIView):
    queryset = Product.objects.order_by('-created_at')
    serializer_class = ProductSerializer


# class ProductPriceView(generics.ListAPIView):
#     queryset = Price.objects.all()
#     serializer_class = PriceSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomerInfoView(generics.ListCreateAPIView):
    queryset = CustomerInfo.objects.all()
    serializer_class = CustomerInfoSerializer


class PurchasedProductView(generics.ListCreateAPIView):
    queryset = PurchasedProduct.objects.all()
    serializer_class = PurchasedProductSerializer


class PurchaseView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    
# class PurchaseView(APIView):
    
#     def get(self, request, format=None):
#         purchase = Purchase.objects.all()
#         purchase_serializer = PurchaseSerializer(purchase, many=True)
#         return Response(purchase_serializer.data)

#     def post(self, request, format=None):
#         data = request.data['products']
#         if data is not None:
#             serializer = PurchaseSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

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


class SliderView(generics.ListAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer


class RecommendedProductView(generics.ListAPIView):
    queryset = RecommendedProduct.objects.all()
    serializer_class = RecommendedProductSerializer


class SaleView(generics.ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class ProductToSaleView(generics.ListCreateAPIView):
    queryset = ProductToSale.objects.all()
    serializer_class = ProductToSaleSerializer