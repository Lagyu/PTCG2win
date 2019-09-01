# Generated by Django 2.1.1 on 2018-09-10 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ArchType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Attack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('damage', models.IntegerField(default=0)),
                ('text', models.CharField(max_length=200)),
                ('text_j', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=50)),
                ('global_id', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('name_j', models.CharField(max_length=100)),
                ('id_in_expansion', models.CharField(max_length=10)),
                ('is_prism_star', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CardBundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('text', models.CharField(default='Comment text is not set.', max_length=10000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.PTCG2winUser')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField()),
                ('mod_date', models.DateTimeField()),
                ('description', models.CharField(max_length=100000)),
                ('arch_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.ArchType')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.PTCG2winUser')),
            ],
        ),
        migrations.CreateModel(
            name='DeckCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('text', models.CharField(default='Invalid deck code.', max_length=24)),
                ('ip', models.CharField(default='0.0.0.0', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Expansion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pub_date', models.DateField()),
                ('code', models.CharField(max_length=10)),
                ('logo_url', models.CharField(max_length=200)),
                ('symbol_url', models.CharField(max_length=200)),
                ('total_cards', models.IntegerField()),
                ('series', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PokemonRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('name_j', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PokemonSpecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('name_j', models.CharField(max_length=10)),
                ('pokedex_number', models.IntegerField()),
                ('evolves_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='decks.PokemonSpecies')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.PokemonRegion')),
            ],
        ),
        migrations.CreateModel(
            name='Rarity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('name_j', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Regulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_available', models.BooleanField(default=False)),
                ('expansions', models.ManyToManyField(to='decks.Expansion')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decks.Region')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Title is not set.', max_length=150)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Weakness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('effect', models.CharField(max_length=10)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decks.Type')),
            ],
        ),
        migrations.CreateModel(
            name='DeckTopic',
            fields=[
                ('topic_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Topic')),
            ],
            bases=('decks.topic',),
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('card_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Card')),
                ('hp', models.IntegerField()),
                ('retreat_cost', models.IntegerField()),
            ],
            bases=('decks.card',),
        ),
        migrations.CreateModel(
            name='Trainers',
            fields=[
                ('card_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Card')),
                ('text', models.CharField(max_length=500)),
            ],
            bases=('decks.card',),
        ),
        migrations.AddField(
            model_name='expansion',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.Region'),
        ),
        migrations.AddField(
            model_name='deck',
            name='regulation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.Regulation'),
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.Region'),
        ),
        migrations.AddField(
            model_name='cardbundle',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.Card'),
        ),
        migrations.AddField(
            model_name='cardbundle',
            name='deck_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decks.Deck'),
        ),
        migrations.AddField(
            model_name='card',
            name='expansion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.Expansion'),
        ),
        migrations.AddField(
            model_name='card',
            name='rarity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.Rarity'),
        ),
        migrations.AddField(
            model_name='card',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.Series'),
        ),
        migrations.AddField(
            model_name='attack',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decks.Card'),
        ),
        migrations.AddField(
            model_name='archtype',
            name='regulation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.Regulation'),
        ),
        migrations.CreateModel(
            name='BasicPokemon',
            fields=[
                ('pokemon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Pokemon')),
            ],
            bases=('decks.pokemon',),
        ),
        migrations.CreateModel(
            name='BreakPokemon',
            fields=[
                ('pokemon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Pokemon')),
                ('evolves_from', models.CharField(max_length=20)),
            ],
            bases=('decks.pokemon',),
        ),
        migrations.CreateModel(
            name='EXPokemon',
            fields=[
                ('pokemon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Pokemon')),
                ('text', models.CharField(max_length=50)),
            ],
            bases=('decks.pokemon',),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('trainers_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Trainers')),
            ],
            bases=('decks.trainers',),
        ),
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('trainers_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Trainers')),
            ],
            bases=('decks.trainers',),
        ),
        migrations.CreateModel(
            name='StageOnePokemon',
            fields=[
                ('pokemon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Pokemon')),
                ('evolves_from', models.CharField(max_length=20)),
            ],
            bases=('decks.pokemon',),
        ),
        migrations.CreateModel(
            name='StageTwoPokemon',
            fields=[
                ('pokemon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Pokemon')),
                ('evolves_from', models.CharField(max_length=20)),
            ],
            bases=('decks.pokemon',),
        ),
        migrations.CreateModel(
            name='Supporter',
            fields=[
                ('trainers_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.Trainers')),
            ],
            bases=('decks.trainers',),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.PokemonSpecies'),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='weakness',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='decks.Weakness'),
        ),
        migrations.AddField(
            model_name='decktopic',
            name='parent_deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decks.Deck'),
        ),
        migrations.AddField(
            model_name='ability',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decks.Pokemon'),
        ),
        migrations.CreateModel(
            name='GXBasicPokemon',
            fields=[
                ('basicpokemon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.BasicPokemon')),
                ('text', models.CharField(max_length=50)),
            ],
            bases=('decks.basicpokemon',),
        ),
        migrations.CreateModel(
            name='GXStageOnePokemon',
            fields=[
                ('stageonepokemon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.StageOnePokemon')),
                ('text', models.CharField(max_length=50)),
            ],
            bases=('decks.stageonepokemon',),
        ),
        migrations.CreateModel(
            name='GXStageTwoPokemon',
            fields=[
                ('stagetwopokemon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.StageTwoPokemon')),
                ('text', models.CharField(max_length=50)),
            ],
            bases=('decks.stagetwopokemon',),
        ),
        migrations.CreateModel(
            name='MegaEXPokemon',
            fields=[
                ('expokemon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='decks.EXPokemon')),
                ('evolves_from', models.CharField(max_length=20)),
            ],
            bases=('decks.expokemon',),
        ),
    ]
