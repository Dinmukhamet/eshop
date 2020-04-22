import factory
from core.models import *

class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand
    
    name = 'Brand Name'
    
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    name = 'Category Name' 

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    name = 'Product Name'
    brand = factory.SubFactory(BrandFactory)
    # category = factory.SubFactory(CategoryFactory)
    price = 250

# class SaleFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Sale
    
#     value = 20