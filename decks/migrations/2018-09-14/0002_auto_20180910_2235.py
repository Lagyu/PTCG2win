# Generated by Django 2.1.1 on 2018-09-10 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeckList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deck_code', models.CharField(max_length=20)),
                ('created_date', models.DateTimeField()),
                ('parent_deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decks.Deck')),
            ],
        ),
        migrations.RemoveField(
            model_name='cardbundle',
            name='deck_list',
        ),
        migrations.AddField(
            model_name='cardbundle',
            name='parent_deck_list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='decks.DeckList'),
            preserve_default=False,
        ),
    ]
