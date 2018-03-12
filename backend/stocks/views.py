from stocks.models import Stock
from stocks.serializers import StockSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import Http404


class StockList(generics.ListCreateAPIView):
    serializer_class = StockSerializer 
    queryset = Stock.objects.all()
    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('ticker', 'name') 


class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StockSerializer 
    queryset = Stock.objects.all() 
    def get_object(self): 
        try:
            return Stock.objects.get(ticker=self.kwargs['ticker'])
        except: 
            raise Http404
