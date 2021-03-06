from django.db import models


class Transaction(models.Model):
    """
        A model for house transactions
    """
    PROPERTY_TYPES = (('S', 'Semi-Detached'), ('D', 'Detached'),
                      ('T', 'Terraced'), ('F', 'Flats'))

    DATE_FILEDS = ["day", "month", "year"]

    ref_id = models.CharField(max_length=100)
    price = models.IntegerField(db_index=True)
    date = models.DateField(db_index=True)
    property_type = models.CharField(max_length=1,
                                     choices=PROPERTY_TYPES,
                                     db_index=True)
    locality = models.CharField(max_length=10, db_index=True)
