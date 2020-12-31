from django import forms
# from django.forms import DecimalField # for class BidForm
# from django.core.validators import DecimalValidator # for class BidForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages


from .models import User, AuctionListings, Watchlist, Bids, Comments

# class CreateForm(forms.Form):
#     title = forms.CharField()
#     description = forms.CharField()
#     start_bid = forms.DecimalField()
#     image_url = forms.ImageField(required=False)

class BidForm(forms.Form):
    bid = forms.DecimalField(max_digits=8, decimal_places=2)

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

# show only active listings
def index(request):
    return render(request, "auctions/index.html", {
        "auctions_list": AuctionListings.objects.filter(isActive=True)
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
        category = request.POST['category']
        # print(title, description, start_bid, image_url)
        user = request.user.username
        ins = AuctionListings(title=title, description=description, start_bid=start_bid, image_url=image_url, isActive=True, user=user, category=category)
        ins.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")

#view to see details of an clicked listing
def listingdetails(request, listing_id):
    user = request.user.username #get the loggin username
    listing_details = AuctionListings.objects.get(pk=listing_id)
    comments = Comments.objects.filter(listing_id=listing_id).values_list('comment', flat=True)

    #see if bids table have cleaned_data
    # try:
    #     latest_bid = Bids.objects.filter(listing_id=listing_id).latest("timestamp")
    #     print(latest_bid.bid)
    # except Bids.DoesNotExist:
    #     print("DoesNotExist")
    #     return HttpResponse("does nt exit. do somethong")
    # watchlist_filter = Watchlist.objects.get(user="neha.mundye", listing_id=1)
    try:
        watchlist_filter = Watchlist.objects.get(user=user, listing_id=listing_id)

        #see if bids table have any cleaned_data
        try:
            latest_bid = Bids.objects.filter(listing_id=listing_id).latest("timestamp")
            # print(latest_bid.bid)
        except Bids.DoesNotExist:
            # print("DoesNotExist")
            return render(request, "auctions/listingdetails.html", {
                "listing_details": listing_details,
                "addOrRmoveButton": "Remove from Watchlist",
                "BidForm": BidForm(),
                "CommentForm": CommentForm(),
                "comments": comments
            })


    except Watchlist.DoesNotExist:
        # print("DoesNotExist")
        try:
            latest_bid = Bids.objects.filter(listing_id=listing_id).latest("timestamp")
            # print(latest_bid.bid)
            return render(request, "auctions/listingdetails.html", {
                "listing_details": listing_details,
                "addOrRmoveButton": "Add to Watchlist",
                "BidForm": BidForm(),
                "latest_bid": latest_bid.bid,
                "CommentForm": CommentForm(),
                "comments": comments
            })
        except Bids.DoesNotExist:
            # print("DoesNotExist")

            return render(request, "auctions/listingdetails.html", {
                "listing_details": listing_details,
                "addOrRmoveButton": "Add to Watchlist",
                "BidForm": BidForm(),
                "CommentForm": CommentForm(),
                "comments": comments
            })

    # listing_details = AuctionListings.objects.get(pk=listing_id)
    # print(listing_details.last_updated_on)
    return render(request, "auctions/listingdetails.html", {
        "listing_details": listing_details,
        "addOrRmoveButton": "Remove from Watchlist",
        "BidForm": BidForm(),
        "latest_bid": latest_bid.bid,
        "CommentForm": CommentForm(),
        "comments": comments
    })
    # return HttpResponse("Yo!")

@login_required(login_url='/login')
def addorremovewatchlist(request, listing_id):
    user = request.user.username #get the loggin username



    if request.method == "POST":
        user = request.user.username #get the loggin username
        # print(user)

        # watchlist_filter = Watchlist.objects.get(user="neha.mundye", listing_id=1)
        # if data already in watchlist, remove it and vice versa.
        try:
            watchlist_filter = Watchlist.objects.get(user=user, listing_id=listing_id)
        except Watchlist.DoesNotExist:
            # print("DoesNotExist")
            ins = Watchlist(user=user, listing_id=listing_id)
            ins.save()
            # print(ins)
            return HttpResponseRedirect(reverse("listingdetails", args=(listing_id,)))

        watchlist_filter.delete()
        # print("removed")
        return HttpResponseRedirect(reverse("listingdetails", args=(listing_id,)))

@login_required(login_url='/login')
def bid(request, listing_id):
    if request.method == "POST":
        # print(request.POST)
        form = BidForm(request.POST)
        user = request.user.username
        # print(form)
        # print(form.is_valid())
        # print(form.errors)
        if form.is_valid():
            bid = form.cleaned_data['bid']
            print(bid)

            try:
                latest_bid = Bids.objects.filter(listing_id=listing_id).latest("timestamp")
            except Bids.DoesNotExist:
                print("DoesNotExist")
                listing_details = AuctionListings.objects.get(pk=listing_id)
                if bid < listing_details.start_bid:
                    messages.error(request, 'The bid should be higher than current bid')
                    return HttpResponseRedirect(reverse("listingdetails", args=(listing_id,)))
                else:
                    ins = Bids(user=user, listing_id=listing_id, bid=bid)
                    ins.save()
                    # print(ins)
                    # return HttpResponse("hello")
                    messages.success(request, 'Your bid has been placed successfully!')
                    return HttpResponseRedirect(reverse("listingdetails", args=(listing_id,)))
            #validate user input
            if bid < latest_bid.bid:
                messages.error(request, 'The bid should be higher than current bid')
                return HttpResponseRedirect(reverse("listingdetails", args=(listing_id,)))
                # return render(request, "auctions/listingdetails.html" )
            else:
                ins = Bids(user=user, listing_id=listing_id, bid=bid)
                ins.save()
                # print(ins)
                # return HttpResponse("hello")
                messages.success(request, 'Your bid has been placed successfully!')
                return HttpResponseRedirect(reverse("listingdetails", args=(listing_id,)))

@login_required(login_url='/login')
def closeauction(request, listing_id):
    if request.method == "POST":
        # TODO: change the isActive flag to False and make the highest bidder the winner of the auction

        user = request.user.username #get the loggin username

        bids_ins = Bids.objects.filter(listing_id=listing_id).latest("timestamp")
        winner = bids_ins.user
        print(winner)

        # change the isActive flag to False
        ins = AuctionListings.objects.get(pk=listing_id)
        ins.isActive = False
        ins.winner = winner
        ins.save(update_fields=['isActive', 'winner'])
        messages.success(request, 'This listing is not active anymore and wont be shown to users!')
        return HttpResponseRedirect(reverse("listingdetails", args=(listing_id,)))

@login_required(login_url='/login')
def addcomment(request, listing_id):
    if request.method == "POST":
        user = request.user.username #get the loggin username
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            ins = Comments(user=user, listing_id=listing_id, comment=comment)
            ins.save()
            return HttpResponseRedirect(reverse("listingdetails", args=(listing_id,)))

@login_required(login_url='/login')
def categories(request):
    categories = AuctionListings.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required(login_url='/login')
def category(request, category):
    filtered_category_id = AuctionListings.objects.filter(category=category).values_list('listing_id', flat=True).distinct()
    return render(request, "auctions/category.html", {
        "auctions_list": AuctionListings.objects.filter(listing_id__in=filtered_category_id),
        "category": category
    })

@login_required(login_url='/login')
def watchlist(request):
    user = request.user.username #get the loggin username
    filtered_listing_id = Watchlist.objects.filter(user=user).values_list('listing_id', flat=True).distinct()
    return render(request, "auctions/watchlist.html", {
        "auctions_list": AuctionListings.objects.filter(listing_id__in=filtered_listing_id)
    })
