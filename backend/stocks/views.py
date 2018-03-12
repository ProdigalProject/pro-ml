from stocks.models import Stock
from stocks.serializers import StockSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import Http404


class StockList(generics.ListCreateAPIView):
    serializer_class = StockSerializer 
    queryset = Stock.objects.all()

class StockDetail(generics.ListAPIView):
    serializer_class = StockSerializer 

    def get_queryset(self): 
        queryset = Stock.objects.filter(ticker=self.kwargs['ticker'])
        if queryset: 
            return queryset
        else: 
            raise Http404
