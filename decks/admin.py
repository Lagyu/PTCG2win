from django.contrib import admin
from .models import Deck, User, ArchType, Expansion, Regulation, Region, Card, CardBundle, PokemonRegion, DeckCode
# Register your models here.


admin.site.register(CardBundle)
admin.site.register(Deck)
admin.site.register(Card)
admin.site.register(User)
admin.site.register(ArchType)
admin.site.register(Expansion)
admin.site.register(Regulation)
admin.site.register(Region)
admin.site.register(PokemonRegion)
admin.site.register(DeckCode)
