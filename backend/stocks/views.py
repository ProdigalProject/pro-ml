from stocks.models import Stock
from stocks.serializers import StockSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


class StockList(generics.ListCreateAPIView):
    serializer_class = StockSerializer 
    queryset = Stock.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('ticker', 'name') 

class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StockSerializer 
    queryset = Stock.objects.all() 
