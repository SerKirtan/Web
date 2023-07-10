from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:auction_id>", views.listing, name="listing"),
    path("listing/<int:auction_id>/bid", views.place_bid, name="place_bid"),
    path("listing/<int:auction_id>/close", views.close_auction, name="close_auction"),
    path("listing/<int:auction_id>/watch", views.watch_auction, name="watch_auction"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("category", views.category, name="category"),
    path("category/<str:type>" , views.openCategory, name="openCategory"),
    path("listing/<int:auction_id>/comment", views.comment, name="comment")
]
