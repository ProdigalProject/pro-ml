from django.conf.urls import url
from django.urls import path, include
from stocks import views

urlpatterns = [
    path('stocks/', views.StockList.as_view()),
    path('stocks/<ticker>/', views.StockDetail.as_view()),
    path('companies/', views.CompanyList.as_view()),
    path('companies/<ticker>/', views.CompanyDetail.as_view()),
    path('prediction/', views.PredictionList.as_view()), 
    path('prediction/<ticker>/', views.PredictionDetail.as_view()), 
]
