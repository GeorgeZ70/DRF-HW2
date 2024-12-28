from rest_framework import serializers

from stocks_products.logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = [
            'product',
            'quantity',
            'price'
        ]


class StockSerializer(serializers.ModelSerializer):

    positions = ProductPositionSerializer(
        many=True
    )

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):

        positions_data = validated_data.pop(
            'positions'
        )

        stock = super().create(
            validated_data
        )

        for position_data in positions_data:
            StockProduct.objects.create(
                stock=stock,
                **position_data
            )

        return stock

    def update(self, instance, validated_data):

        positions_data = validated_data.pop(
            'positions'
        )

        stock = super().update(
            instance,
            validated_data
        )

        for position_data in positions_data:
            obj, created = StockProduct.objects.update_or_create(
                stock=stock,
                product=position_data.get('product'),
                defaults={
                    'stock': stock,
                    'product': position_data.get('product'),
                    'quantity': position_data.get('quantity'),
                    'price': position_data.get('price')
                }
            )

        return stock