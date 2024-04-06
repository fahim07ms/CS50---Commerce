from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

# one for auction listings, one for bids, and one for comments

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    starting_bid = models.IntegerField()
    url = models.URLField(blank=True)
    dateCreated = models.DateTimeField(default=datetime.now, blank=True, )

    def __str__(self):
        return f"{self.id}. {self.title}"

# They should be able to specify a title for the listing, a text-based description, and what the starting bid should be.
# Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).


