from unittest.mock import patch

import pytest

from shortener.models import CODE_LENGTH, ShortenedURL
from shortener.services import (
    BASE62_CHARACTERS,
    create_short_url,
    generate_random_code,
)


def test_generate_random_code_length_and_charset() -> None:
    code = generate_random_code(length=CODE_LENGTH)
    assert len(code) == CODE_LENGTH
    assert all(char in BASE62_CHARACTERS for char in code)


@pytest.mark.django_db
def test_create_short_url_success() -> None:
    target = "https://example.com/target-path"
    instance = create_short_url(target)

    assert instance.pk is not None
    assert instance.original_url == target
    assert len(instance.short_code) == CODE_LENGTH


@pytest.mark.django_db
def test_create_short_url_creates_distinct_entries_for_same_url() -> None:
    target = "https://example.com/same-url"
    first = create_short_url(target)
    second = create_short_url(target)

    assert first.pk != second.pk
    assert first.original_url == second.original_url
    assert first.short_code != second.short_code
    assert ShortenedURL.objects.filter(original_url=target).count() == 2


@pytest.mark.django_db
def test_create_short_url_collision_retry() -> None:
    ShortenedURL.objects.create(
        original_url="https://example.com/existing",
        short_code="colld1",
    )
    with patch(
        "shortener.services.generate_random_code",
        side_effect=["colld1", "unq002"],
    ):
        created = create_short_url("https://example.com/new-url")
        assert created.short_code == "unq002"


@pytest.mark.django_db
def test_create_short_url_exhaustion_raises_runtime_error() -> None:
    ShortenedURL.objects.create(
        original_url="https://example.com/existing",
        short_code="colld1",
    )
    with (
        patch("shortener.services.generate_random_code", return_value="colld1"),
        pytest.raises(
            RuntimeError,
            match="Failed to generate a unique short code after maximum attempts.",
        ),
    ):
        create_short_url("https://example.com/blocked", max_attempts=3)
