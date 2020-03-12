from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.views import APIView, Response
from rest_framework.exceptions import APIException
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Max
from django.http import JsonResponse
from .permissions import *
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
            response = {"Error": {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  "type": "Internal Server Error",
                                  "message": 'Brand with id {} does not exist'.format(pk)}}
            raise APIException(response)
            # return JsonResponse({'status': 'false', 'message': 'Brand with id {} does not exist'.format(pk)}, status=500    )

    def get(self, request, pk, format=None):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryView(generics.ListAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class CategoryDetailView(APIView):

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            response = {"Error": {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  "type": "Internal Server Error",
                                  "message": 'Category with id {} does not exist'.format(pk)}}
            raise APIException(response)

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class ProductPriceFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['brand', 'min_price', 'max_price']


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductPriceFilter


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
            response = {"Error": {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  "type": "Internal Server Error",
                                  "message": 'Product with id {} does not exist'.format(pk)}}
            raise APIException(response)

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
            response = {"Error": {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  "type": "Internal Server Error",
                                  "message": "Products can not be empty. Fill 'product' and 'count' fields."}}
            raise APIException(response)

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
            response = {"Error": {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  "type": "Internal Server Error",
                                  "message": "Purchase with id {} does not exist".format(pk)}}
            raise APIException(response)

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


class SaleView(generics.ListCreateAPIView):
    permission_classes = [IsPostOrIsAuthenticated,]
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class ProductToSaleView(generics.ListAPIView):
    queryset = ProductToSale.objects.all()
    serializer_class = ProductToSaleSerializer


# class SaleBundleView(generics.ListCreateAPIView):
#     queryset = SaleBundle.objects.all()
#     serializer_class = SaleBundleSerializer


class ProductToSaleBundleView(generics.ListAPIView):
    queryset = ProductToSaleBundle.objects.all()
    serializer_class = ProductToSaleBundleSerializer


class SaleBundleView(APIView):
    permission_classes = [IsPostOrIsAuthenticated]

    def get(self, request, format=None):
        # if user.is_admin:
        salebundle = SaleBundle.objects.all()
        serializer = SaleBundleSerializer(salebundle, many=True)
        return Response(serializer.data)
        # else:
        #     response = {"Error": {"status": status.HTTP_403_FORBIDDEN,
        #                           "forbidden": "You don’t have permission to access [directory] on this server",
        #                           "message": "Authentication credentials were not provided."}}
        #     raise APIException(response)

    def post(self, request, format=None):
        products = request.data.get('products')

        if len(products) is 0:
            response = {"Error": {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  "type": "Internal Server Error",
                                  "message": "Products can not be empty. Fill 'category' and 'product'fields."}}
            raise APIException(response)

        elif len(products) is 1:
            response = {"Error": {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  "type": "Internal Server Error",
                                  "message": "You can't add only one product to bundle."}}
            raise APIException(response)

        serializer = SaleBundleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
