import factory
from core.models import *

class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand
    
    name = 'Brand Name'

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    name = 'Product Name'
    brand = factory.SubFactory(BrandFactory)