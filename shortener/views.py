from typing import Any

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shortener.models import ShortenedURL
from shortener.serializers import ShortenInputSerializer
from shortener.services import create_short_url


class ShortenURLView(APIView):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = ShortenInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_url: str = str(serializer.validated_data["url"])
        shortened = create_short_url(original_url=target_url)

        short_url: str = request.build_absolute_uri(
            reverse("short-url-redirect", kwargs={"code": shortened.short_code})
        )
        return Response({"short_url": short_url}, status=status.HTTP_201_CREATED)


class ExpandURLView(APIView):
    def get(self, request: Request, code: str, *args: Any, **kwargs: Any) -> Response:
        shortened = ShortenedURL.objects.filter(short_code=code).first()
        if shortened is None:
            return Response(
                {"detail": "Shortened URL not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"original_url": shortened.original_url},
            status=status.HTTP_200_OK,
        )


class ShortURLRedirectView(View):
    def get(
        self, request: HttpRequest, code: str, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        shortened = ShortenedURL.objects.filter(short_code=code).first()
        if shortened is None:
            return HttpResponseNotFound("Shortened URL not found.")
        return HttpResponseRedirect(shortened.original_url)
