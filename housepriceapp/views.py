import django_filters
from django.shortcuts import render
from django.db.models import Avg, Max, Min, Count
from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer, TransactionAggregateSerializer
from rest_framework import generics


def index(request):
    return render(request, 'index.html', {})


class TransactionFilter(django_filters.FilterSet):
    from_date = django_filters.DateTimeFilter(name="date", lookup_type='gte')
    to_date = django_filters.DateTimeFilter(name="date", lookup_type='lte')

    class Meta:
        model = Transaction
        fields = ['locality', 'from_date', 'to_date']


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_class = TransactionFilter


class TransactionAggregateView(generics.ListAPIView):
    """
    A view that returns the count of active users.
    """

    serializer_class = TransactionAggregateSerializer
    filter_class = TransactionFilter

    def get_queryset(self):
        groups = self.request.QUERY_PARAMS.get('groupby', None)
        groups = groups.split(",")

        queryset = Transaction.objects

        values = []
        extras = {}

        for group in groups:
            if group == "month":
                extras["year"] = "extract('year' from date)"
                extras["month"] = "extract('month' from date)"
                values.append("year")
                values.append("month")

            elif group == "price":
                bins = self.request.QUERY_PARAMS.get('bins', None)

                qs = Transaction.objects

                f = TransactionFilter(self.request.QUERY_PARAMS, queryset=qs)

                min_price = f.qs.aggregate(Min('price')).get('price__min')
                max_price = f.qs.aggregate(Max('price')).get('price__max')

                extra = "width_bucket(price, " + str(min_price) + ", " + \
                        str(max_price) + ", " + bins + ")"
                extras["price_bin"] = extra

                values.append("price_bin")

            else:
                values.append(group)

        if extras:
            queryset = queryset.extra(extras)
        if values:
            queryset = queryset.values(*values)

        queryset = queryset.annotate(Avg('price'),
                                     Min('price'),
                                     Max('price'),
                                     Count('id'))

        return queryset
