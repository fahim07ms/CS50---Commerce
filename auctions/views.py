from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "url"]
        
        widgets = {
            "title" : forms.TextInput(attrs={"class":"form-control"}),
            "description" : forms.Textarea(attrs={"class":"form-control"}),
            "starting_bid": forms.NumberInput(attrs={"class":"form-control"}),
            "url": forms.URLInput(attrs={"label": "URL","class":"form-control"}),
        }

    def __inti__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            instances = form.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": ListingForm(),
            })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": listing.product_comments.all(),
    })

def bid(request, listing_id):
    if request.method == "POST":
        user = User.objects.get(pk=int(request.POST["user_id"]))
        listing = Listing.objects.get(pk=listing_id)
        amount = int(request.POST["bid"])

        c_bid = listing.current_bid

        if (c_bid is None and amount >= listing.starting_bid) or (amount > c_bid):
            bid = Bid(person=user, listing=listing, amount=amount)
            bid.save()

            listing.current_bid = amount
            listing.save()

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Bid placed."
            })

        if c_bid is not None: 
            message = "Less than current bid!"
        else:
            message = "Less than starting bid!"

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": message,
        })
    
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def comment(request, listing_id):
    if request.method == "POST":
        user = User.objects.get(pk=int(request.POST["user_id"]))
        listing = Listing.objects.get(pk=listing_id)
        text = request.POST["comment"]

        comment = Comment(person=user, listing=listing, comment=text)
        comment.save()

        return HttpResponseRedirect(reverse("listing", kwargs={
            "listing_id": listing_id,
        }))