from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction_listing, Category, Watchlist, Bid, Comment

from decimal import Decimal


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction_listing.objects.filter(active=True)
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

def auction_view(request, listing_id):
    try:
        listing = Auction_listing.objects.get(id=listing_id)
    except Auction_listing.DoesNotExist:
        raise Http404("Listing not found.")
    
    is_watchlist = (
        request.user.is_authenticated
        and Watchlist.objects.filter(user=request.user, auction=listing).exists()
    )

    if listing.active == 1:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_watchlist": is_watchlist
        })
    else:
        return render(request, "auctions/listing_inactive.html", {
            "listing": listing
        })

def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all()
        })
    
    # POST
    user = request.user
    title = request.POST["title"]
    description = request.POST["description"]
    starting_bid = Decimal(request.POST["bid"])
    image_url = request.POST["image_url"]
    category_id = request.POST.get("category")
    category = Category.objects.get(id=category_id) if category_id else None

    listing = Auction_listing(
        user=user,
        title=title,
        description=description,
        starting_bid=starting_bid,
        category=category,
        image_url=image_url
    )
    listing.save()

    return HttpResponseRedirect(reverse("auction_view", args=[listing.id]))

def watchlist(request):
    if request.method == "GET":
        return render(request, "auctions/watchlist.html", {
            "listings": Watchlist.objects.filter(user=request.user)
        })

def watchlist_toggle(request, listing_id):
    listing = Auction_listing.objects.get(id=listing_id)

    existing = Watchlist.objects.filter(user=request.user, auction=listing)
    if existing.exists():
        existing.delete()
    else:
        Watchlist(user=request.user, auction=listing).save()

    return HttpResponseRedirect(reverse("auction_view", args=[listing.id]))

def place_bid(request, listing_id):
    if request.method == "POST":
        curr_bid = Decimal(request.POST["bid"])
        user = request.user
        listing = Auction_listing.objects.get(id=listing_id)

        top_bid = listing.bids.order_by("-value").first()

        if top_bid:
            invalid = curr_bid <= top_bid.value
            message = "Bid has to be bigger than the current bid."
        else:
            invalid = curr_bid < listing.starting_bid
            message = "Bid has to be at least as large as the starting bid."

        if invalid:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": message
            })

        Bid(listing=listing, user=user, value=curr_bid).save()
        return render(request, "auctions/listing.html", {
                "listing": listing
            })

def close(request, listing_id):
    if request.method == "POST":
        listing = Auction_listing.objects.get(id=listing_id)

        if listing.active == 1:
            if listing.user != request.user:
                return HttpResponseRedirect(reverse("auction_view", args=[listing.id]))

            listing.active = 0
            listing.winner = listing.biggest_bidder()

            listing.save()

            return render(request, "auctions/listing_inactive.html", {
                "listing": listing
            })
        
        else:
            return render(request, "auctions/listing_inactive.html", {
                "listing": listing
            })

def comment(request, listing_id):
    user = request.user
    content = request.POST["content"]
    listing = Auction_listing.objects.get(id=listing_id)

    Comment(user=user, listing=listing, content=content).save()
    return HttpResponseRedirect(reverse("auction_view", args=[listing.id]))

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category(request, cat_id):
    return render(request, "auctions/categories_specific.html", {
        "category": Category.objects.get(id=cat_id),
        "listings": Auction_listing.objects.filter(category=Category.objects.get(id=cat_id), active=True)
    })
