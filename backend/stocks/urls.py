from django.conf.urls import url
from django.urls import path, include
from stocks import views

urlpatterns = [
    path('stocks/', views.StockList.as_view()),
    path('stocks/update', views.run_update_all),
    path('stocks/<ticker>/', views.StockDetail.as_view()),
    path('stocks/<ticker>/runexpr', views.run_experiment_return_results),
    path('stocks/<ticker>/update', views.run_update)
]
