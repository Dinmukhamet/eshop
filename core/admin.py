from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price',
                    'image', 'brand')
    fieldsets = [
        (None, {'fields': (('name', 'description'),
                           'price', 'image', 'brand')})
    ]

class SubcategoryToProductAdmin(admin.ModelAdmin):
    list_filter = ('subcategory',)

admin.site.register(Product, ProductAdmin)
admin.site.register(SubcategoryToProduct, SubcategoryToProductAdmin)