from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListings

# class CreateForm(forms.Form):
#     title = forms.CharField()
#     description = forms.CharField()
#     start_bid = forms.DecimalField()
#     image_url = forms.ImageField(required=False)

def index(request):
    return render(request, "auctions/index.html", {
        "auctions_list": AuctionListings.objects.all()
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

def create(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        start_bid = request.POST['start_bid']
        image_url = request.FILES['image_url']
        print(title, description, start_bid, image_url)
        ins = AuctionListings(title=title, description=description, start_bid=start_bid, image_url=image_url, isActive=True)
        ins.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")
