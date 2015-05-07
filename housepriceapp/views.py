from django.shortcuts import render
from django.db.models import Avg, Max, Min, Count
from rest_framework import viewsets, generics
from .models import Transaction
from .filters import TransactionFilter
from .exceptions import GroupByFieldError, NoDataError
from .serializers import TransactionSerializer, TransactionAggregateSerializer
import re


def index(request):
    """The main view
    Args:
        request: the http request
    Returns:
        The rendered page
    """
    return render(request, 'index.html', {})


class TransactionViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint that allows transactions to be viewed.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_class = TransactionFilter
    allowed_methods = ('GET',)


# The list of allowed group by fields
ALLOWED_GROUPS = Transaction._meta.get_all_field_names() \
    + Transaction.DATE_FILEDS


class TransactionAggregateView(generics.ListAPIView):
    """
    REST API endpoint that allows transactions aggregates to be viewed.
    This includes average, min, max and count group by given parameters
    """

    serializer_class = TransactionAggregateSerializer
    filter_class = TransactionFilter
    page_size = None
    allowed_methods = ('GET',)

    def get_queryset(self):
        """
        Build the queryset given the query parameters
        """

        # starting from all of the transactions
        queryset = Transaction.objects

        # the list of field to be grouped
        groupby = []
        # any extra field to be computed
        extras = {}

        groups = self.request.QUERY_PARAMS.getlist('groupby', None)
        bins = self.request.QUERY_PARAMS.getlist('bins', None)

        if groups:
            for field in groups:

                # if we have a group by bins we need to extract the bin for
                # each row
                group_by_bins = re.match("^(.*)_bin$", field)

                if group_by_bins:
                    groupby_field, field = field, group_by_bins.group(1)
                else:
                    groupby_field = field

                if field not in ALLOWED_GROUPS:
                    raise GroupByFieldError

                groupby.append(groupby_field)

                if field in Transaction.DATE_FILEDS:
                    # extract year and month from the date
                    extras[field] = "extract('" + field + "' from date)"

                if group_by_bins:
                    # we need to have as many bins as there are bin groups
                    if not bins:
                        raise GroupByFieldError

                    field_bins = bins.pop()

                    # get the min, max
                    qs = Transaction.objects

                    f = TransactionFilter(self.request.QUERY_PARAMS,
                                          queryset=qs)

                    min_field = f.qs.aggregate(Min(field)) \
                        .get(field + '__min')

                    max_field = f.qs.aggregate(Max(field)) \
                        .get(field + '__max')

                    if not min_field or not max_field:
                        raise NoDataError

                    # get the bin for a range between min and max excluded
                    extras[groupby_field] = "width_bucket(" + field + ", " \
                                            + str(min_field) + ", " \
                                            + str(max_field + 1) + ", " + field_bins \
                                            + ")"

        # add the extra fields to the queryset
        if extras:
            queryset = queryset.extra(extras)

        # group by and order by the grouped terms
        if groupby:
            queryset = queryset.values(*groupby)
            queryset = queryset.order_by(*groupby)

        # the aggregate functions to be returned
        queryset = queryset.annotate(Avg('price'),
                                     Min('price'),
                                     Max('price'),
                                     Count('id'))
        return queryset
