# Generated by Django 2.1.1 on 2018-09-14 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0002_auto_20180915_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='id_in_expansion',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
