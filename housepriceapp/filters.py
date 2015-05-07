from .models import Transaction
import django_filters


class TransactionFilter(django_filters.FilterSet):
    """The set of filters to be applied on the Transaction model
    """
    date_from = django_filters.DateTimeFilter(name="date", lookup_type='gte')
    date_to = django_filters.DateTimeFilter(name="date", lookup_type='lt')

    class Meta:
        model = Transaction
        fields = ['locality', 'date_from', 'date_to']
