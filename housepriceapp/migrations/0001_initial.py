# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField()),
                ('date', models.DateField()),
                ('property_type', models.CharField(max_length=1)),
                ('locality', models.CharField(max_length=10)),
            ],
        ),
    ]
