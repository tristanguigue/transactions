from django.conf.urls import url, patterns
from housepriceapp import views
from django.conf import settings

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/$', views.api_root),
    url(r'^api/transactions/$',
        views.TransactionViewSet.as_view({'get': 'list'}),
        name='transactions'),
    url(r'^api/transactions/aggregate/$',
        views.TransactionAggregateView.as_view(),
        name='transactions-aggregate')

]

if not settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$',
                             'django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT}))
