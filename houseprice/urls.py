from django.conf.urls import url
from housepriceapp import views

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/transactions/$',
        views.TransactionViewSet.as_view({'get': 'list'})),
    url(r'^api/transactions/aggregate/$',
        views.TransactionAggregateView.as_view(),
        name='transactions-aggregate')

]
