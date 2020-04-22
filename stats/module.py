from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import Sum, Count
import datetime
from core.models import *
from jet.dashboard import modules
from django.utils.translation import ugettext_lazy as _


class Stats:
    @classmethod
    def get_purchase_stats_for_dashboard(cls) -> list:
        queryset = Product.objects.all().values('total_purchase', 'price')
        total_purchases = sum(i['total_purchase'] for i in queryset)
        total_revenue = sum(i['price'] for i in queryset) * total_purchases
        queryset = PurchasedProduct.objects.all().values('product__price', 'count')
        average_bill = round(sum(i['product__price'] for i in queryset)/sum(i['count'] for i in queryset), 2)

        stats = [
            {
                'name': _('Total Purchases'),
                'value': total_purchases
            },
            {
                'name': _('Total Revenue'),
                'value': total_revenue
            },
            {
                'name': _('Average Bill'),
                'value': average_bill
            }
        ]

        return stats

    @classmethod
    def get_top_products_stats_for_dashboard(cls) -> dict:
        queryset = PurchasedProduct.objects.values('created_at__date').annotate(day=TruncDay(
            'created_at__date')).values('day').annotate(c=Sum('count')).values('day', 'c').order_by('day')
        labels = []
        data = []

        for product in queryset:
            labels.append(product['day'].strftime('%Y-%m-%d'))
            data.append(product['c'])

        stats = {'labels':labels, 'data':data}

        return stats

    @classmethod
    def get_brand_stats_for_dashboard(cls) -> dict:
        labels = []
        data = []

        queryset = Product.objects.values('brand__name').annotate(
            total=Sum('total_purchase')).values('brand__name', 'total').order_by('-total')[:5]

        for product in queryset:
            labels.append(product['brand__name'])
            data.append(product['total'])

        stats = {'labels':labels, 'data':data}

        return stats
    @classmethod
    def get_products_by_total_purchase_for_dashboard(cls) -> dict:
        labels = []
        data = []
        short_name = []

        queryset = Product.objects.values(
            'name', 'total_purchase').order_by('total_purchase')

        for product in queryset:
            labels.append(product['name'])
            data.append(product['total_purchase'])
            short_name.append(product['name'].split()[0])

        stats = {'labels':labels, 'data':data, 'short_name': short_name}

        return stats
    
    @classmethod
    def get_revenue_for_dashboard(cls) -> dict:
        labels = []
        data = []
        # queryset = PurchasedProduct.objects.values('created_at__date').annotate(day=TruncDay(
        #     'created_at__date')).values('day').annotate(c=Sum('count')).values('day', 'c').order_by('day')
        queryset = PurchasedProduct.objects.values('created_at__date').annotate(month=TruncMonth('created_at__date')).values('month').annotate(quantity=Sum('count')).annotate(price=Sum('product__price')).values('month', 'quantity', 'price').order_by('month')

        for product in queryset:
            labels.append(product['month'].strftime('%b'))
            data.append(int(product['quantity'])*int(product['price']))

        stats = {'labels':labels, 'data':data}

        return stats

class StatsModule(modules.DashboardModule):
    title = _('Statistics')
    template = 'stats/chart.html'

    def __init__(self, title=None, model=None, context=None, **kwargs):
        super().__init__(title, model, context, **kwargs)
        self.purchase_stats = Stats.get_purchase_stats_for_dashboard()
        self.brand_stats = Stats.get_brand_stats_for_dashboard()
        self.top_products_stats = Stats.get_top_products_stats_for_dashboard
        self.products_stats = Stats.get_products_by_total_purchase_for_dashboard()
        self.revenue_stats = Stats.get_revenue_for_dashboard()
