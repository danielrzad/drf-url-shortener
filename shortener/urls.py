from django.urls import path

from shortener.views import ExpandURLView, ShortenURLView

urlpatterns = [
    path("shorten/", ShortenURLView.as_view(), name="shorten-url"),
    path("expand/<str:code>/", ExpandURLView.as_view(), name="expand-url"),
]
