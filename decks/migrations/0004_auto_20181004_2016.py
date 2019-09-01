# Generated by Django 2.1.1 on 2018-10-04 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0003_auto_20180915_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='image_url',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='decklist',
            name='deck_code',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
