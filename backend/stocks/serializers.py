from rest_framework import serializers
from stocks.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("name", "ticker", "high", "low",
                  "opening", "closing", "volume", "date")
