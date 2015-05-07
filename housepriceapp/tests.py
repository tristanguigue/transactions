from rest_framework.test import APITestCase
from rest_framework import status


class TransactionTests(APITestCase):
    fixtures = ['transactions.json']

    def setUp(self):
        pass

    def test_get_transactions(self):
        response = self.client.get('/api/transactions/', {})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 4)

    def test_get_transactions_filters(self):
        response = self.client.get('/api/transactions/', {'locality': 'SO40'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_transactions_filters_date(self):
        response = self.client.get('/api/transactions/',
                                   {'date_from': '2013-04-01'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_transactions_aggregate(self):
        response = self.client.get('/api/transactions/aggregate/', {})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 4)
        self.assertIn('price_avg', response.data["results"][0])

    def test_get_transactions_aggregate_groupby(self):
        response = self.client.get('/api/transactions/aggregate/',
                                   {'groupby': 'month'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

        response = self.client.get('/api/transactions/aggregate/',
                                   {'groupby': 'year'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

        response = self.client.get('/api/transactions/aggregate/',
                                   {'groupby': 'property_type'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_transactions_aggregate_multiple_groupby(self):
        response = self.client.get('/api/transactions/aggregate/',
                                   {'groupby': ['year', 'property_type']})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

    def test_get_transactions_aggregate_groupby_bins(self):
        response = self.client.get('/api/transactions/aggregate/',
                                   {'groupby': 'price_bin', 'bins': 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["results"][0]['price_avg'] <
                        response.data["results"][1]['price_avg'])

    def test_get_transactions_aggregate_error(self):
        response = self.client.get('/api/transactions/aggregate/',
                                   {'groupby': 'blabla'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_transactions_aggregate_no_content(self):
        response = self.client.get('/api/transactions/aggregate/',
                                   {'groupby': 'price_bin',
                                    'bins': 2,
                                    'date_from': '2015-06-01'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
