from django.urls import path
from stats import views

urlpatterns = [
    # path('chart/', views.bar_chart, name='bar-chart'),
    path('chart/', views.pie_chart, name='pie-chart'),
]
