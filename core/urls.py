from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core import views

schema_view = get_schema_view(
    openapi.Info(
        title="E-SHOP API",
        default_version='v1',
        description="",
        terms_of_service="",
        contact=openapi.Contact(email="d.igisinov@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# router = DefaultRouter()
# router.register(r'category', views.CategoryView)
# router.register(r'subcategory', views.SubcategoryView)
# router.register(r'subcategory_to_product', views.SubcategoryToProductView)
# router.register(r'brand', views.BrandView)
# router.register(r'product', views.ProductView)
# router.register(r'contact', views.ContactView)
# router.register(r'purchased_product', views.PurchasedProductView)
# router.register(r'purchase', views.PurchaseView)
# router.register(r'rating', views.RatingView)
# router.register(r'comment', views.CommentView)
# router.register(r'comment_rating', views.CommentRatingView)

urlpatterns = [
    # path('', include(router.urls)),
    path('brand/', views.BrandView.as_view(), name='brand'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('purchased_product/', views.PurchasedProductView.as_view(), name='purchased_product'),
    path('purchase/', views.PurchaseView.as_view(), name='purchase'),
    path('product_rating/', views.RatingView.as_view(), name='product_rating'),
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('comment_rating/', views.CommentRatingView.as_view(), name='comment_rating'),
    path('favourite/', views.FavouriteView.as_view(), name='favourite'),
    path('favourite_product', views.FavouriteProductView.as_view(), name='favourite_product'),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)