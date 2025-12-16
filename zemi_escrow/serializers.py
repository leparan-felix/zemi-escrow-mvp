from rest_framework import serializers

class OrderCreateSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    product_description = serializers.CharField(max_length=255)
