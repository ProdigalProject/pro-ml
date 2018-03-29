from stocks.models import Stock, Company, Prediction
from stocks.serializers import StockSerializer, CompanySerializer, PredictionSerializer
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django.http import Http404, JsonResponse


class StockList(generics.ListCreateAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    filter_backends = (OrderingFilter,) 
    ordering_fields = ('date',)


class StockDetail(generics.ListAPIView):
    serializer_class = StockSerializer 
    filter_backends = (OrderingFilter,)
    ordering_fields = ('date',)

    def get_queryset(self): 
        queryset = Stock.objects.filter(ticker=self.kwargs['ticker'])
        if queryset: 
            return queryset
        else: 
            raise Http404


class CompanyList(generics.ListCreateAPIView): 
    serializer_class = CompanySerializer 
    queryset = Company.objects.all()


class CompanyDetail(generics.ListAPIView):
    serializer_class = CompanySerializer 

    def get_queryset(self): 
        queryset = Company.objects.filter(ticker=self.kwargs['ticker'])
        if queryset: 
            return queryset
        else: 
            raise Http404


class PredictionList(generics.ListCreateAPIView): 
    serializer_class = PredictionSerializer 
    queryset = Prediction.objects.all()


class PredictionDetail(generics.ListAPIView):
    serializer_class = PredictionSerializer 

    def get_queryset(self): 
        queryset = Prediction.objects.filter(ticker=self.kwargs['ticker'])
        if queryset: 
            return queryset
        else: 
            raise Http404


def run_experiment_return_results(request, ticker):
    """
    Runs experiment module on request from API endpoint. Then, returns experiment results packed in json list.
    :param request: Http request
    :param ticker: Ticker symbol passed from endpoint
    :return: JSON list of experiment results
    """
    expr_result = [100, 101, 102, 103, 104]  # numbers to be returned from experiment module
    results = []
    for index in range(1, 6):
        results.append({"id": index, "ticker": ticker, "value": expr_result[index - 1]})
    return JsonResponse(results, status=200, safe=False)


def run_update(request, ticker):
    """
    Runs update on specified ticker symbol on request from API endpoint. For daily update automation purpose.
    :param request: Http request
    :param ticker: Ticker symbol passed from endpoint
    :return: JSON response containing operation result.
    """
    result = Stock.update_by_ticker(ticker)
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
    result = Stock.update_all()
    return JsonResponse(result, status=200)
