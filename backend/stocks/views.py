from stocks.models import Stock
from stocks.serializers import StockSerializer
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django.http import Http404, JsonResponse
from .utilities import StockHistoryUpdater, ExperimentManager, AlphaAPICaller
import requests
from rest_framework_bulk import ListBulkCreateAPIView
from django.db import connection 
import time


class StockList(generics.ListCreateAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    filter_backends = (OrderingFilter,) 
    ordering_fields = ('date',)


class StockDetail(generics.ListAPIView):
    serializer_class = StockSerializer 
    filter_backends = (OrderingFilter,)
    ordering_fields = ('date',)
    api = "http://prodigal-ml.azurewebsites.net/stocks/" 

    def get_queryset(self): 
        queryset = Stock.objects.filter(ticker=self.kwargs['ticker'])
        if queryset: 
            return queryset
        else: 
            ticker = self.kwargs['ticker'] 
            alpha = AlphaAPICaller() 
            json_data = alpha.get_compact_date(ticker)
            
            if len(json_data) > 0: 
                cur = connection.cursor()
                query = """INSERT INTO stocks_stock(ticker, high, low,\
                        opening, closing, volume, date)\
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                my_tuples = [tuple(x.values()) for x in json_data]
                cur.executemany(query, my_tuples)
                mdata = requests.get(self.api + ticker).json()
                return mdata
            else: 
                raise Http404

def run_experiment_return_results(request, ticker):
    """
    Runs experiment module on request from API endpoint. Then, returns experiment results packed in json list.
    :param request: Http request
    :param ticker: Ticker symbol passed from endpoint
    :return: JSON list of experiment results
    """
    results = ExperimentManager.run_experiment(ticker)
    if results == -1:
        return JsonResponse({"result": "Error", "error": "Failed to find matching company"}, status=404)
    else:
        return JsonResponse(results, status=200, safe=False)


def run_update(request, ticker):
    """
    Runs update on specified ticker symbol on request from API endpoint. For daily update automation purpose.
    :param request: Http request
    :param ticker: Ticker symbol passed from endpoint
    :return: JSON response containing operation result.
    """
    result = StockHistoryUpdater.update_by_ticker(ticker)
    if result == 0:
        return JsonResponse({"result": "OK"}, status=200)
    elif result == 1:
        return JsonResponse({"result": "Error", "error": "Record already exists"}, status=200)
    else:
        return JsonResponse({"result": "Error", "error": "Failed to find matching company"}, status=404)


def run_update_all(request):
    """
    Runs update on all ticker symbols in database on request from API endpoint. For daily update automation purpose.
    :param request: Http request
    :return: JSON response containing operation result on each ticker.
    """
    result = StockHistoryUpdater.update_all()
    return JsonResponse(result, status=200)
