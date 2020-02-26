from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView, Response
from rest_framework.exceptions import APIException
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Max

# from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import *

# Create your views here.


# class BrandView(generics.ListAPIView):
#     queryset = Brand.objects.all()
#     serializer_class = BrandSerializer

class BrandView(APIView):

    def get(self, request, format=None):
        # brands = [brand.name for brand in Brand.objects.all()]
        instance = Brand.objects.all()
        serializer = BrandSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandDetailView(APIView):

    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise APIException('Brand with id {} does not exist'.format(pk))

    def get(self, request, pk, format=None):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(APIView):

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise APIException('Category with id {} does not exist'.format(pk))

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


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


class ProductDetailView(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise APIException('Product with id {} does not exist'.format(pk))

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CustomerInfoView(generics.ListCreateAPIView):
    queryset = CustomerInfo.objects.all()
    serializer_class = CustomerInfoSerializer


class PurchasedProductView(generics.ListCreateAPIView):
    queryset = PurchasedProduct.objects.all()
    serializer_class = PurchasedProductSerializer


# class PurchaseView(generics.ListCreateAPIView):
#     queryset = Purchase.objects.all()
#     serializer_class = PurchaseSerializer

class PurchaseView(APIView):

    def get(self, request, format=None):
        purchase = Purchase.objects.all()
        purchase_serializer = PurchaseSerializer(purchase, many=True)
        return Response(purchase_serializer.data)

    def post(self, request, format=None):
        products = request.data.get('products')

        if len(products) is 0:
            raise APIException("Products can not be empty. Fill 'product' and 'count' fields.")

        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PurchaseDetailView(APIView):

    def get_object(self, pk):
        try:
            return Purchase.objects.get(pk=pk)
        except Purchase.DoesNotExist:
            raise APIException('Purchase with id {} does not exist'.format(pk))

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = PurchaseSerializer(product)
        return Response(serializer.data)


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


class ProductToSaleView(generics.ListAPIView):
    queryset = ProductToSale.objects.all()
    serializer_class = ProductToSaleSerializer
