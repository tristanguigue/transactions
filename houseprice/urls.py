from django.conf.urls import url, include
from housepriceapp import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'^transactions/$', views.TransactionViewSet)
# router.register(r'^transactions/aggregate/$', views.TransactionAggregateView)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/', include(router.urls)),
    url(r'^api/transactions/aggregate/$',
        views.TransactionAggregateView.as_view(),
        name='transactions-aggregate')

]
