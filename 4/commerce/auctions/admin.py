from django.contrib import admin

from .models import User, AuctionListings, Watchlist, Bids, Comments

# Register your models here.
class UserWatchlist(admin.ModelAdmin):
    list_display =("user", "listing_id")

class Bidslist(admin.ModelAdmin):
    list_display =("user", "listing_id", "bid", "timestamp")

admin.site.register(User)
admin.site.register(AuctionListings)
admin.site.register(Watchlist, UserWatchlist)
admin.site.register(Bids, Bidslist)
admin.site.register(Comments)
