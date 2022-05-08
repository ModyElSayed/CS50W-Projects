from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect

from .forms import *
from .models import *


def common_context(request):
    choices = AuctionListings.Category
    number_of_lists = Watchlist.objects.filter(user_id=request.user.id, watchlist__status='Active')
    context = {'number_of_lists': len(number_of_lists), 'choices': choices}
    return context


def index(request):
    active_listings = AuctionListings.objects.filter(status='Active').order_by('-date_created')
    context = {'active_listings': active_listings, **common_context(request)}
    return render(request, "auctions/index.html", context)


def category(request, listings_type):
    listings_type_data = AuctionListings.objects.filter(category=listings_type).order_by('-date_created')
    context = {'listings_type': listings_type_data, **common_context(request)}
    return render(request, 'auctions/category.html', context)


@login_required
def listing_details(request, listing_type):
    listing_bid = AuctionListings.objects.get(title=listing_type)
    number_of_bidders = ListingBids.objects.filter(listing=listing_bid, listing_status='Active')
    in_watchlist = Watchlist.objects.filter(user_id=request.user.id, watchlist_id=listing_bid.pk)
    bid_form = BidForm(request.POST or None)
    comment_form = add_comment(request, listing_bid.pk)
    comments = get_comments(request, listing_bid)
    context = {'comment_form': comment_form, "listing": listing_bid, 'bid_form': bid_form,
               'in_watchlist': len(in_watchlist), 'number_of_bidders': len(number_of_bidders), 'comments': comments,
               **common_context(request)}

    if bid_form.is_valid():
        try:
            print('I am here')
            bid_price = bid_form.cleaned_data.get('bid')

            if bid_price < listing_bid.final_bid:
                raise ValueError()

            old_bidder = ListingBids.objects.filter(user_id=request.user.id, listing=listing_bid,
                                                    listing_status='Active')

            if old_bidder.exists():
                old_bidder.update(bid_price=bid_price)

            else:
                ListingBids.objects.create(user_id=request.user.id, listing=listing_bid, bid_price=bid_price,
                                           listing_status='Active')

            listing_bid.final_bid = bid_price
            listing_bid.save()
            return redirect('auctions:index')
        except ValueError:
            return render(request, "auctions/listing_details.html", {
                **context,
                "message": f'Your bid should be higher than ',
                'final_bid': listing_bid.final_bid,
            })

    return render(request, 'auctions/listing_details.html', context)


@login_required
def add_comment(request, listing_id):
    comment_form = CommentForm(request.POST or None)
    listing = AuctionListings.objects.get(pk=listing_id)

    if comment_form.is_valid():
        comment = comment_form.cleaned_data.get('comment_area')
        ListingComments.objects.create(user_id=request.user.id, listing=listing, comments=comment)
        return redirect('auctions:listing_details', listing.title)

    return comment_form


@login_required
def get_comments(request, listing):
    comments = ListingComments.objects.filter(user_id=request.user.id, listing=listing).order_by('-date_added')
    return comments


@login_required
def close_bid(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    listing_bids = list(ListingBids.objects.filter(listing=listing).order_by('-bid_price'))
    listing.status = AuctionListings.Status.INACTIVE

    if len(listing_bids) > 0:
        listing_bids[0].listing_status = ListingBids.ListingStatus.WON
        listing_bids[0].save()

        for bid_index in range(1, len(listing_bids)):
            listing_bids[bid_index].listing_status = ListingBids.ListingStatus.LOST
            listing_bids[bid_index].save()

    listing.save()
    Watchlist.objects.filter(watchlist_id=listing).delete()
    return redirect('auctions:index')


@login_required(redirect_field_name='')
def watchlist(request):
    watchlist_data = Watchlist.objects.filter(user_id=request.user.id,
                                              watchlist__status='Active').order_by('-date_added')
    context = {'watchlist_data': watchlist_data, **common_context(request)}
    return render(request, "auctions/watchlist.html", context)


@login_required
def add_to_watchlist(request, listing_id):
    if request.method == 'POST':
        Watchlist.objects.create(user_id=request.user.id, watchlist_id=listing_id)
        listing = AuctionListings.objects.get(pk=listing_id)
        return redirect('auctions:listing_details', listing.title)
    return redirect('auctions:index')


@login_required
def delete_from_watchlist(request, listing_id):
    if request.method == 'POST':
        Watchlist.objects.get(user_id=request.user.id, watchlist_id=listing_id).delete()
        return redirect('auctions:watchlist')
    return redirect('auctions:index')


@login_required(redirect_field_name='')
def create_listings(request):
    create_listing_form = ListingsForm(request.POST or None)

    if create_listing_form.is_valid():
        new_listing = create_listing_form.clean()
        AuctionListings.objects.create(description=new_listing.get('description'), category=new_listing.get('category'),
                                       starting_bid=new_listing.get('starting_bid'), title=new_listing.get('title'),
                                       image_url=new_listing.get('image_url'), user=request.user, status='Active',
                                       final_bid=new_listing.get('starting_bid'))
        return redirect('auctions:index')

    context = {'listing_form': create_listing_form, **common_context(request)}
    return render(request, 'auctions/create_listings.html', context)


@login_required
def winning_listings(request):
    wins = ListingBids.objects.filter(user_id=request.user.id, listing_status='Won')
    context = {'wins': wins, **common_context(request)}
    return render(request, 'auctions/winning_listings.html', context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('auctions:index')
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                **common_context(request)
            })
    else:

        return render(request, "auctions/login.html", common_context(request))


def logout_view(request):
    logout(request)
    return redirect('auctions:index')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                **common_context(request)
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                **common_context(request)
            })
        login(request, user)
        return redirect('auctions:index')
    else:
        return render(request, "auctions/register.html", common_context(request))
