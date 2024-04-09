from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.conf import settings

class User(AbstractUser):
    pass

# one for auction listings, one for bids, and one for comments

class Listing(models.Model):
    CATEGORIES = {
        "Others": "No Category",
        "Broomstick": "Broomstick",
        "Wand": "Wand",
        "Cloak": "Cloak",
        "Clothes": "Clothes",
        "Hat": "Hat"
    }
    
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    starting_bid = models.IntegerField()
    url = models.URLField(blank=True) 
    category = models.CharField(max_length=20, choices=dict(sorted(CATEGORIES.items())), default="None")
    dateCreated = models.DateTimeField(default=datetime.now, blank=True,)
    current_bid = models.IntegerField(default=None, null=True)


    def __str__(self):
        return f"{self.id}. {self.title}"

class Bid(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product_bids")
    amount = models.IntegerField()
    dateBidded = models.DateTimeField(default=datetime.now, blank=True,)

    def __str__(self):
        return f"{self.person} bids on {self.listing}"


class Comment(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product_comments")
    comment = models.CharField(max_length=200)
    dateCommented = models.DateTimeField(default=datetime.now, blank=True,)

    def __str__(self):
        return f"{self.person} comments on {self.listing}"
