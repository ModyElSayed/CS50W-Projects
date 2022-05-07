from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class AuctionListings(models.Model):
    class Category(models.TextChoices):
        FASHION = 'Fashion'
        TOYS = 'Toys'
        ELECTRONICS = 'Electronics'
        HOME = 'Home'
        WOMEN = 'Women'
        MEN = 'Men'

    class Status(models.TextChoices):
        ACTIVE = 'Active'
        INACTIVE = 'Inactive'

    class ErrorMessages:
        STARTING_BID = 'Starting bid should be 0 or greater'

    title = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=256)
    starting_bid = models.FloatField(validators=[MinValueValidator(0, message=ErrorMessages.STARTING_BID)],
                                     default=0.0)
    final_bid = models.FloatField()
    category = models.CharField(max_length=len(Category.ELECTRONICS), choices=Category.choices,
                                default=Category.FASHION)
    image_url = models.URLField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=len(Status.INACTIVE), choices=Status.choices, default=Status.ACTIVE)
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return f'{self.title}: ${self.final_bid}'


class ListingComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name='listing')
    comments = models.CharField(max_length=256)
    date_added = models.DateTimeField(auto_now=True)


class ListingBids(models.Model):
    class ListingStatus(models.TextChoices):
        WON = 'Won'
        LOST = 'Lost'
        ACTIVE = 'Active'

    class ErrorMessages:
        BID_PRICE_ERROR = 'Starting bid should be greater than the final bid'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name='auction_listings')
    bid_price = models.FloatField()
    listing_status = models.CharField(max_length=len(ListingStatus.ACTIVE), choices=ListingStatus.choices,
                                      default=ListingStatus.ACTIVE)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name='listings')
    date_added = models.DateTimeField(auto_now=True)
