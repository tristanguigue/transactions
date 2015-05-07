from .models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    """
    The serializer for the Transaction model specifies which field we want
    to return
    """
    class Meta:
        model = Transaction
        fields = ('price', 'locality', 'date', 'property_type')


class TransactionAggregateSerializer(serializers.ModelSerializer):
    """
    The serializer for the aggregates needs to declare both the fields from
    the transaction model and the extra fields we have created for the
    aggregate
    """
    class Meta:
        model = Transaction
        fields = ('count', 'price_avg', 'price_min', 'price_max',
                  'month', 'year', 'price_bin',
                  'property_type', 'locality')

    price_avg = serializers.IntegerField(source='price__avg')
    price_min = serializers.IntegerField(source='price__min')
    price_max = serializers.IntegerField(source='price__max')
    count = serializers.IntegerField(source='id__count')

    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    property_type = serializers.SerializerMethodField()
    locality = serializers.SerializerMethodField()
    price_bin = serializers.SerializerMethodField()

    def get_extra_field(self, obj, field):
        if type(obj) is dict:
            return obj.get(field, None)
        else:
            return None

    def get_price_bin(self, obj):
        return self.get_extra_field(obj, 'price_bin')

    def get_locality(self, obj):
        return self.get_extra_field(obj, 'locality')

    def get_property_type(self, obj):
        return self.get_extra_field(obj, 'property_type')

    def get_month(self, obj):
        return self.get_extra_field(obj, 'month')

    def get_year(self, obj):
        return self.get_extra_field(obj, 'year')
