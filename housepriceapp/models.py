from django.db import models


class Transaction(models.Model):
    """
        A model for house transactions
    """
    PROPERTY_TYPES = (('S', 'Semi-Detached'), ('D', 'Detached'),
                      ('T', 'Terraced'), ('F', 'Flats'))

    DATE_FILEDS = ["day", "month", "year"]

    price = models.IntegerField()
    date = models.DateField()
    property_type = models.CharField(max_length=1, choices=PROPERTY_TYPES)
    locality = models.CharField(max_length=10)
