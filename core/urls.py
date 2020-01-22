from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register(r'category', views.CategoryView)
router.register(r'subcategory', views.SubcategoryView)
router.register(r'subcategory_to_product', views.SubcategoryToProductView)
router.register(r'brand', views.BrandView)
router.register(r'product', views.ProductView)
router.register(r'contact', views.ContactView)
router.register(r'purchased_product', views.PurchasedProductView)
router.register(r'purchase', views.PurchaseView)

urlpatterns = [
    path('', include(router.urls)),
]