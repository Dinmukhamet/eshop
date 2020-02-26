from django.contrib import admin
from django.db.models import Count, Sum, DateTimeField, Min, Max
from django.db.models.functions import Trunc
from django.contrib.sessions.models import Session
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from .models import *


# Register your models here.
def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'week'
    return 'month'


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category', 'brand')
    list_display = ('name', 'price', 'brand')
    fieldsets = [
        (None, {'fields': ('name', 'price', 'category', 'brand')})
    ]


@admin.register(SaleSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list.html'
    list_filter = (
        'product__category',
    )
    date_hierarchy = 'created_at'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('count'),
            'total_sales': Sum('product__price'),
        }

        response.context_data['summary'] = list(
            qs.values('product__name').annotate(
                **metrics).order_by('-total_sales')
        )

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        period = get_next_in_date_hierarchy(request, self.date_hierarchy)

        response.context_data['period'] = period

        summary_over_time = qs.annotate(period=Trunc('created_at', period, output_field=DateTimeField(
        ))).values('period').annotate(total=Sum('product__price')).order_by('period')

        summary_range = summary_over_time.aggregate(
            low=Min('total'), high=Max('total'))

        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)

        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': ((x['total'] or 0) - low) / (high - low) * 100
            if high > low else 0,
        } for x in summary_over_time]

        return response


class CustomerInfoAdmin(admin.ModelAdmin):
    list_filter = ('purchase',)
    list_display = ('name', 'email', 'phone_number', 'address', 'comment')
    fieldsets = [
        (None, {'fields': (('name', 'email', 'phone_number', 'address', 'comment'))})
    ]


class SaleAdmin(admin.ModelAdmin):
    list_filter = ('date_from', 'date_to')
    list_display = ('date_from', 'date_to', 'value', 'display_products_to_sale')
    fieldsets = [
        (None, {'fields': (('date_to', 'value'))})
    ]

class ProductToSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale', 'product', 'old_price', 'new_price')

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


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_customer_info', 'display_customer_email', 'display_purchased_product', 'total_sum')
    
class RecommendedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'display_recommendedproduct')

admin.site.register(Session, SessionAdmin)
admin.site.register(Slider)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(CustomerInfo, CustomerInfoAdmin)
admin.site.register(RecommendedProduct, RecommendedProductAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(ProductToSale, ProductToSaleAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PurchasedProduct)
