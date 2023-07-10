from django.contrib import admin
from .models import *

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id" , "item", "category" , "price", "user" )

class BidAdmin(admin.ModelAdmin):
    list_display = ("id" , "auction" , "user" , "amount")

class CategoryAdmin(admin.ModelAdmin):
    list_display =("id" , "name")

class CommentAdmin(admin.ModelAdmin):
    list_display= ("id" , "user", "comment")

admin.site.register(User)
admin.site.register(Auction_Listing , ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)