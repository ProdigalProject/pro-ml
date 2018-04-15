from django.conf.urls import url
from django.urls import path, include
from stocks import views

urlpatterns = [
    path('stocks/', views.view_all_stocks),
    path('stocks/update', views.run_update_all),
    path('stocks/<ticker>/', views.view_stock_detail),
    path('stocks/<ticker>/runexpr', views.run_experiment_return_results),
    path('stocks/<ticker>/update', views.run_update)
]
