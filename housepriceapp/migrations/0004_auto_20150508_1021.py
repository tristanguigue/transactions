# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('housepriceapp', '0003_auto_20150508_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='locality',
            field=models.CharField(max_length=10, db_index=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='price',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='property_type',
            field=models.CharField(db_index=True, max_length=1, choices=[(b'S', b'Semi-Detached'), (b'D', b'Detached'), (b'T', b'Terraced'), (b'F', b'Flats')]),
        ),
    ]
