# Generated by Django 2.0.4 on 2017-08-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20170801_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engagement',
            name='year',
            field=models.IntegerField(choices=[(2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017)], default=2018, verbose_name='Year'),
        ),
    ]
