# Generated by Django 2.1.1 on 2018-10-04 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0004_auto_20181004_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expansion',
            name='symbol_url',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
