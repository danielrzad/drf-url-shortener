import pytest
from rest_framework import status
from rest_framework.test import APIClient

from shortener.models import ShortenedURL


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
def test_full_shorten_expand_and_redirect_flow(api_client: APIClient) -> None:
    target_url = "https://example.com/very-very/long/url/even-longer"

    shorten_response = api_client.post(
        "/api/v1/shorten/",
        data={"url": target_url},
        format="json",
    )
    assert shorten_response.status_code == status.HTTP_201_CREATED
    data = shorten_response.json()
    assert "short_url" in data
    assert list(data.keys()) == ["short_url"]

    short_url: str = data["short_url"]
    code: str = short_url.rstrip("/").split("/")[-1]
    assert len(code) == 6

    expand_response = api_client.get(f"/api/v1/expand/{code}/")
    assert expand_response.status_code == status.HTTP_200_OK
    assert expand_response.json() == {"original_url": target_url}

    redirect_response = api_client.get(f"/shrt/{code}/")
    assert redirect_response.status_code == status.HTTP_302_FOUND
    assert redirect_response.headers["Location"] == target_url


@pytest.mark.django_db
def test_shorten_same_url_creates_distinct_short_urls(
    api_client: APIClient,
) -> None:
    target_url = "https://example.com/repeated-target"

    first_response = api_client.post(
        "/api/v1/shorten/",
        data={"url": target_url},
        format="json",
    )
    assert first_response.status_code == status.HTTP_201_CREATED

    second_response = api_client.post(
        "/api/v1/shorten/",
        data={"url": target_url},
        format="json",
    )
    assert second_response.status_code == status.HTTP_201_CREATED

    first_url: str = first_response.json()["short_url"]
    second_url: str = second_response.json()["short_url"]

    assert first_url != second_url
    assert ShortenedURL.objects.filter(original_url=target_url).count() == 2


@pytest.mark.django_db
def test_not_found_handling(api_client: APIClient) -> None:
    expand_response = api_client.get("/api/v1/expand/unknown404/")
    assert expand_response.status_code == status.HTTP_404_NOT_FOUND

    redirect_response = api_client.get("/shrt/unknown404/")
    assert redirect_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_validation_errors(api_client: APIClient) -> None:
    invalid_url_res = api_client.post(
        "/api/v1/shorten/",
        data={"url": "invalid-url"},
        format="json",
    )
    assert invalid_url_res.status_code == status.HTTP_400_BAD_REQUEST

    empty_body_res = api_client.post(
        "/api/v1/shorten/",
        data={},
        format="json",
    )
    assert empty_body_res.status_code == status.HTTP_400_BAD_REQUEST

    legacy_field_res = api_client.post(
        "/api/v1/shorten/",
        data={"original_url": "https://example.com"},
        format="json",
    )
    assert legacy_field_res.status_code == status.HTTP_400_BAD_REQUEST
