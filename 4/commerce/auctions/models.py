from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64, blank=True)
    start_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.ImageField(null=True, blank=True)
    isActive = models.BooleanField(blank=True)
    last_updated_on = models.DateTimeField(default=now)
    category = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.title}, {self.start_bid}, {self.isActive}, {self.category}, {self.image_url}"
