from .models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ('price', 'locality', 'date', 'property_type')


class TransactionAggregateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('count', 'price_avg', 'price_min', 'price_max',
                  'month', 'year', 'property_type', 'locality', 'price_bin')

    price_avg = serializers.IntegerField(source='price__avg')
    price_min = serializers.IntegerField(source='price__min')
    price_max = serializers.IntegerField(source='price__max')
    count = serializers.IntegerField(source='id__count')

    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    property_type = serializers.SerializerMethodField()
    locality = serializers.SerializerMethodField()
    price_bin = serializers.SerializerMethodField()

    def get_price_bin(self, obj):
        return obj.get('price_bin', None)

    def get_locality(self, obj):
        return obj.get('locality', None)

    def get_property_type(self, obj):
        return obj.get('property_type', None)

    def get_month(self, obj):
        return obj.get('month', None)

    def get_year(self, obj):
        return obj.get('year', None)
