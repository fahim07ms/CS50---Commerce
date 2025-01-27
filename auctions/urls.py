from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>/", views.listing, name="listing"),
    path("listings/<int:listing_id>/bid/", views.bid, name="bid"),
    path("listings/<int:listing_id>/comment/", views.comment, name="comment"),
    path("listings/watchlist/", views.watchlist, name="watchlist"),
    path("listings/categories/<str:category>/", views.categories, name="categories"),
]
