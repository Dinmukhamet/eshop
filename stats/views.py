from django.shortcuts import render
from core.models import *
from django.template import loader
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay

import datetime

def pie_chart(request):
    '''
                                Top Brand
    '''
    labels = []
    data = []

    queryset = Product.objects.values('brand__name').annotate(total=Sum('total_purchase')).values('brand__name', 'total').order_by('-total')

    for product in queryset:
        labels.append(product['brand__name'])
        data.append(product['total'])
    '''
                                Bestseller

    '''
    labelsBar = []
    dataBar = []
    # querysetBar = PurchasedProduct.objects.annotate(day=TruncDay('created_at')).values('day').annotate(q=Count('product_id')).annotate(c=Count('count')).values('day', 'q','c').order_by('day')
    
    querysetBar = PurchasedProduct.objects.values('created_at__date').annotate(day=TruncDay('created_at__date')).values('day').annotate(c=Sum('count')).values('day','c').order_by('day')

    r = []
    d = []

    for p in querysetBar:
        r.append(p['day'].strftime('%Y-%m-%d'))   
        d.append(p['c'])

    labelsBar = r
    dataBar = d
    '''
                                Unpopular product
    '''   
    unpopularLabels = []
    unpopularData = []

    queryset = Product.objects.values('name', 'total_purchase').order_by('total_purchase')

    for p in queryset:
        unpopularLabels.append(p['name'])
        unpopularData.append(p['total_purchase'])

    # template = loader.get_template('stats/pie_chart.html')
    return render(request, 'stats/chart.html', {
        'brand_labels': labels,
        'brand_data': data,
        'purchase_labels': labelsBar,
        'purchase_data': dataBar,
        'unpopular_labels': unpopularLabels,
        'unpopular_data': unpopularData
    })
    
# def bar_chart(request):
#     labelsBar = []
#     dataBar = []

#     querysetBar = PurchasedProduct.objects.filter(created_at__year='2020')

#     from datetime import timedelta, date

#     def daterange(date1, date2):
#         for n in range(int ((date2 - date1).days)+31):
#             yield date1 + timedelta(n)

#     start_dt = date(2020, 1, 1)
#     end_dt = date(2020, 12, 30)
#     labels = [dt.strftime("%Y-%m-%d") for dt in daterange(start_dt, end_dt)]
    
#     for purchase in queryset:
#         data.append(purchase.count)
#     # template = loader.get_template('stats/pie_chart.html')
#     return render(request, 'stats/chart.html', {
#         'purchase_labels': labels,
#         'purchase_data': data,
#     })

