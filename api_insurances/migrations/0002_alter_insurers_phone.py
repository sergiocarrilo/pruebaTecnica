# Generated by Django 3.2.6 on 2021-08-24 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_insurances', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurers',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Detail'),
        ),
    ]
