from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Auction_Listing, Bid, Category, Comment, User
from .forms import ListingForm, BidForm, CommentForm

def index(request):
    listings = Auction_Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings
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


def listing(request, auction_id):
    if request.user.is_anonymous:
        return render(request, "auctions/login_required.html")
    try:
        listing = Auction_Listing.objects.get(pk=auction_id)
    except:
        return HttpResponse("Entry does not exist")
        
    isWatching = False    
    if listing in request.user.watchlist.all():
        isWatching = True

    context = {}
    context["ended"] = False 
    if listing.is_finished():
        context["ended"] = True

    context["isWatching"] = isWatching
    context["listing"] = listing
    context["bid_form"] = BidForm()
    context["comment_form"] = CommentForm()
    context["messages"]: messages.get_messages(request)

    return render(request, "auctions/listing.html", context)


def place_bid(request, auction_id):
    bid_form = BidForm(request.POST or None)
    if bid_form.is_valid():
        user = request.user
        auction = Auction_Listing.objects.get(pk=auction_id)
        new_bid = bid_form.save(commit=False)
        current_bids = Bid.objects.filter(auction=auction)
        is_highest_bid = all(new_bid.amount > n.amount for n in current_bids)
        is_valid_first_bid = new_bid.amount >= auction.price

        if is_highest_bid and is_valid_first_bid:
            new_bid.auction = auction
            new_bid.user = user
            new_bid.save()
            messages.success(request, 'Bid placed successfully.')
        else:
            messages.error(request, 'Invalid bid value.')
    else:
        messages.error(request, 'Form submission error.')

    url = reverse('listing', kwargs={'auction_id': auction_id })
    return HttpResponseRedirect(url)

@login_required
def create_listing(request):
    form = ListingForm(request.POST or None)
    if form.is_valid():
        new_listing = form.save(commit=False)
        new_listing.user = request.user
        new_listing.save()

        url = reverse('listing', kwargs={'auction_id': new_listing.id})
        return HttpResponseRedirect(url)

    else:
        return render(request, "auctions/create_listing.html", {
            'form': form
        })
    
def close_auction(request, auction_id):
    auction = Auction_Listing.objects.get(pk=auction_id)
    if(request.user == auction.user):
        auction.ended_manually = True
        auction.save()

    url = reverse('listing' , kwargs={'auction_id' : auction_id})
    return HttpResponseRedirect(url)

def watch_list(request):
    return render(request, "auctions/watch_list.html", {
        "listings" : request.user.watchlist.all(),
    })

def watch_auction(request, auction_id):
    watchlist = request.user.watchlist
    auction = Auction_Listing.objects.get(pk=auction_id)

    if not auction in watchlist.all():
        watchlist.add(auction)
        messages.success(request, "Added to watchlist")
    else:
        watchlist.remove(auction)
        messages.success(request, "Removed from watchlist")

    url = reverse('listing', kwargs={'auction_id':auction_id})
    return HttpResponseRedirect(url)

def category(request):
    category = Category.objects.all()
    return render(request, "auctions/category.html", {
        "categories" : category
    })

def openCategory(request, type):
    category = get_object_or_404(Category, name=type)
    auctions = Auction_Listing.objects.filter(category=category)
    return render(request, "auctions/openCategory.html", {
        "auctions" : auctions
    })

def comment(request, auction_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.auction = Auction_Listing.objects.get(pk=auction_id)
        new_comment.save()
    url = reverse('listing', kwargs={'auction_id':auction_id})
    return HttpResponseRedirect(url)