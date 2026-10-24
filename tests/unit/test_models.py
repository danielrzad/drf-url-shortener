import pytest
from django.db import IntegrityError

from shortener.models import ShortenedURL


@pytest.mark.django_db
def test_shortened_url_creation() -> None:
    link = ShortenedURL.objects.create(
        original_url="https://example.com/test",
        short_code="xyz123",
    )
    assert link.pk is not None
    assert link.original_url == "https://example.com/test"
    assert link.short_code == "xyz123"
    assert str(link) == "xyz123 -> https://example.com/test"


@pytest.mark.django_db
def test_shortened_url_unique_short_code() -> None:
    ShortenedURL.objects.create(
        original_url="https://example.com/first",
        short_code="samecd",
    )
    with pytest.raises(IntegrityError):
        ShortenedURL.objects.create(
            original_url="https://example.com/second",
            short_code="samecd",
        )


@pytest.mark.django_db
def test_shortened_url_allows_duplicate_original_url() -> None:
    first = ShortenedURL.objects.create(
        original_url="https://example.com/duplicate",
        short_code="code01",
    )
    second = ShortenedURL.objects.create(
        original_url="https://example.com/duplicate",
        short_code="code02",
    )
    assert first.pk != second.pk
    assert first.original_url == second.original_url
    assert first.short_code != second.short_code
