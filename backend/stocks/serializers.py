from rest_framework import serializers
from stocks.models import Stock, Company, Prediction
from rest_framework_bulk import BulkListSerializer


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("ticker", "high", "low",
                  "opening", "closing", "volume", "date")


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("company_name", "ticker", "exchange")


class PredictionSerializer(BulkListSerializer, serializers.ModelSerializer): 
    class Meta: 
        list_serializer_class = BulkListSerializer
        model = Prediction 
        fields = ("ticker", "prediction", "date_ran_experiment") 

