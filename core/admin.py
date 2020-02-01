from django.contrib import admin
from .models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category', 'brand')
    list_display = ('name', 'description', 'price',
                    'image', 'brand')
    fieldsets = [
        (None, {'fields': (('name', 'description'),
                           'price', 'image', 'category', 'brand')})
    ]


class PurchasedProductAdmin(admin.ModelAdmin):
    list_filter = ('purchase',)
    list_display = ('name', 'price', 'count', 'total')

    fieldsets = [
        (None, {'fields': ('name', 'price', 'count', 'total')})
    ]


admin.site.register(Slider)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(RecommendedProduct)
admin.site.register(Sale)
admin.site.register(Product, ProductAdmin)
admin.site.register(PurchasedProduct, PurchasedProductAdmin)
