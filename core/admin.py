from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category', 'brand')
    list_display = ('name', 'description',
                    'image', 'brand')
    fieldsets = [
        (None, {'fields': (('name', 'description'), 'image', 'category', 'brand')})
    ]


# class PurchasedProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'count', 'total')

#     fieldsets = [
#         (None, {'fields': ('name', 'price', 'count', 'total')})
#     ]

class ContactAdmin(admin.ModelAdmin):
    list_filter = ('purchase',)
    list_display = ('name', 'email', 'phone_number', 'address', 'comment')
    fieldsets = [
        (None, {'fields': (('name', 'email', 'phone_number', 'address', 'comment'))})
    ]

class SaleAdmin(admin.ModelAdmin):
    list_filter = ('date_from', 'date_to')
    list_display = ('date_from', 'date_to', 'value')
    fieldsets = [
        (None, {'fields': (('date_to', 'value', 'products'))})
    ]

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('parent',)
    list_display = ('name', 'parent')
    fieldsets = [
        (None, {'fields': (('name', 'parent'))})
    ]

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

admin.site.register(Session, SessionAdmin)
admin.site.register(Slider)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Price)
admin.site.register(Contact, ContactAdmin)
admin.site.register(RecommendedProduct)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PurchasedProduct)
# , PurchasedProductAdmin)
