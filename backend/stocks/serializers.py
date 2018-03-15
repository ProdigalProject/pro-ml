from rest_framework import serializers
from stocks.models import Stock, Company, Prediction


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("name", "ticker", "high", "low",
                  "opening", "closing", "volume", "date")

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("company_name", "ticker", "exchange")

class PredictionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Prediction 
        fields = ("ticker", "prediction", "date_ran_experiment") 
