from rest_framework import serializers
from stocks.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("ticker", "high", "low",
                  "opening", "closing", "volume", "date")
