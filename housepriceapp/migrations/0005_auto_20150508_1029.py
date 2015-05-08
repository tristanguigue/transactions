# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def import_csv_sql(csv_file):
    return "COPY housepriceapp_transaction(ref_id, price, date,\
            locality, property_type, drop1, drop2, drop3,\
            drop4, drop5, drop6, drop7, drop8, drop9, drop10)\
            FROM '" + csv_file + "' \
            DELIMITER ',' CSV ENCODING 'windows-1251';"


class Migration(migrations.Migration):

    dependencies = [
        ('housepriceapp', '0004_auto_20150508_1021'),
    ]

    operations = [
        # This is unfortunately the only way to import only a subset of the CSV
        # columns
        # see http://stackoverflow.com/questions/12618232/copy-a-few-of-the-columns-of-a-csv-file-into-a-table
        migrations.RunSQL("ALTER TABLE housepriceapp_transaction\
                           ADD COLUMN drop1 character varying,\
                           ADD COLUMN drop2 character varying,\
                           ADD COLUMN drop3 character varying,\
                           ADD COLUMN drop4 character varying,\
                           ADD COLUMN drop5 character varying,\
                           ADD COLUMN drop6 character varying,\
                           ADD COLUMN drop7 character varying,\
                           ADD COLUMN drop8 character varying,\
                           ADD COLUMN drop9 character varying,\
                           ADD COLUMN drop10 character varying;"),

        migrations.RunSQL(
            import_csv_sql('/tmp/pp-2010.csv')),
        migrations.RunSQL(
            import_csv_sql('/tmp/pp-2011.csv')),
        migrations.RunSQL(
            import_csv_sql('/tmp/pp-2012.csv')),
        migrations.RunSQL(
            import_csv_sql('/tmp/pp-2013.csv')),
        migrations.RunSQL(
            import_csv_sql('/tmp/pp-2014.csv')),
        migrations.RunSQL(
            import_csv_sql('/tmp/pp-2015.csv')),

        migrations.RunSQL("UPDATE housepriceapp_transaction\
                           SET locality = (regexp_split_to_array(locality, E'\\\\s+'))[1];"),

        migrations.RunSQL("ALTER TABLE housepriceapp_transaction\
                           DROP COLUMN drop1,\
                           DROP COLUMN drop2,\
                           DROP COLUMN drop3,\
                           DROP COLUMN drop4,\
                           DROP COLUMN drop5,\
                           DROP COLUMN drop6,\
                           DROP COLUMN drop7,\
                           DROP COLUMN drop8,\
                           DROP COLUMN drop9,\
                           DROP COLUMN drop10;"),
    ]
