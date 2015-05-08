# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('housepriceapp', '0002_auto_20150430_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='ref_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='property_type',
            field=models.CharField(max_length=1, choices=[(b'S', b'Semi-Detached'), (b'D', b'Detached'), (b'T', b'Terraced'), (b'F', b'Flats')]),
        ),
    ]
