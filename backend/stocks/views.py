from stocks.models import Stock
from stocks.serializers import StockSerializer
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django.http import Http404


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
