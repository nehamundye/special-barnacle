from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listingdetails, name="listingdetails"),
    path("<int:listing_id>/addorremovewatchlist", views.addorremovewatchlist, name="addorremovewatchlist"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/closeauction", views.closeauction, name="closeauction"),
    path("<int:listing_id>/addcomment", views.addcomment, name="addcomment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist")
]
