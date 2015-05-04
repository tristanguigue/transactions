from django.db import models


class Transaction(models.Model):
    PROPERTY_TYPES = (('S', 'Semi-Detached'), ('D', 'Detached'),
                      ('T', 'Terraced'), ('F', 'Flats'))

    price = models.IntegerField()
    date = models.DateField()
    property_type = models.CharField(max_length=1, choices=PROPERTY_TYPES)
    locality = models.CharField(max_length=10)
