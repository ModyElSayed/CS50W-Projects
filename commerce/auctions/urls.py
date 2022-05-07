from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("listing_details/<str:listing_type>", views.listing_details, name="listing_details"),
    path("close_bid/<int:listing_id>", views.close_bid, name="close_bid"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("delete_from_watchlist/<int:listing_id>", views.delete_from_watchlist, name="delete_from_watchlist"),
    path("category/<str:listings_type>", views.category, name="category"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("create_listings/", views.create_listings, name="create_listings"),
    path("winning_listings/", views.winning_listings, name="winning_listings"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
]
