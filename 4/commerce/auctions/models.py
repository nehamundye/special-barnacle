from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    listing_id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64, blank=True)
    start_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.ImageField(null=True, blank=True)
    isActive = models.BooleanField(default=True)
    last_updated_on = models.DateTimeField(default=now)
    category = models.CharField(max_length=64, blank=True)
    winner = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.listing_id}, {self.user},{self.title}, {self.start_bid}, {self.isActive}, {self.category}, {self.image_url}, {self.isActive}"

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()

    def __str__(self):
        return f"user: {self.user}, listing_id: {self.listing_id}"

class Bids(models.Model):
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"user: {self.user}, listing_id: {self.listing_id}, bid: {self.bid}, timestamp: {self.timestamp}"

class Comments(models.Model):
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    comment = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"user: {self.user}, listing_id: {self.listing_id}, comment: {self.comment}, timestamp: {self.timestamp}"
