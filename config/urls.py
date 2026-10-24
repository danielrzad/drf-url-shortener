from django.urls import include, path

from shortener.views import ShortURLRedirectView

urlpatterns = [
    path("api/v1/", include("shortener.urls")),
    path("shrt/<str:code>/", ShortURLRedirectView.as_view(), name="short-url-redirect"),
]
