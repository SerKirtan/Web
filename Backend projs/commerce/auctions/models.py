from datetime import datetime , timedelta 
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=64)

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return f"{self.name}"
    
class Auction_Listing(models.Model):
    item = models.CharField(max_length=128)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_listings")
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auction_listings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    DURATIONS = (
        (3, "Three Days"),
        (7, "One Week"),
        (14, "Two Weeks"),
        (28, "Four Weeks")
    )
    duration         = models.IntegerField(choices=DURATIONS)
    ended_manually   = models.BooleanField(default=False)
    watchers         = models.ManyToManyField(
                          User,
                          blank=True,
                          related_name="watchlist")
    
    class Meta:
        ordering = ('-end_time',)

    def __str__(self):
        return f"Auction #{self.id}: {self.item} ({self.user.username})"

    def save(self, *args, **kwargs):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(days=self.duration)
        super().save(*args, **kwargs) # call existing save() method

    def is_finished(self):
        if self.ended_manually or self.end_time < timezone.now():
            return True
        else:
            return False


class Bid(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="bids")

    class Meta:
        ordering = ('-amount',)

    def __str__(self):
        return f"Bid #{self.id}: {self.amount} on {self.auction.item} by {self.user.username}"

class Comment(models.Model):
    comment = models.CharField(max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="comments")
    time = datetime.now()

    def __str__(self):
        return f"{self.id} - {self.user} --> {self.auction}"