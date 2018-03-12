from django.conf.urls import url
from django.urls import path, include
from stocks import views

urlpatterns = [
    path('stocks/', views.StockList.as_view()),
    path('stocks/<ticker>/', views.StockDetail.as_view()),
    #path('stocks/<ticker>/prediction/', views.StockDetail.as_view()),
]
