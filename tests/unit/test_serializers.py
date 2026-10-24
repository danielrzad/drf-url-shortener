from shortener.serializers import ShortenInputSerializer


def test_shorten_input_serializer_valid_url() -> None:
    serializer = ShortenInputSerializer(data={"url": "https://example.com/valid"})
    assert serializer.is_valid()
    assert serializer.validated_data == {"url": "https://example.com/valid"}


def test_shorten_input_serializer_missing_url() -> None:
    serializer = ShortenInputSerializer(data={})
    assert not serializer.is_valid()
    assert "url" in serializer.errors


def test_shorten_input_serializer_invalid_url() -> None:
    serializer = ShortenInputSerializer(data={"url": "not-a-valid-url"})
    assert not serializer.is_valid()
    assert "url" in serializer.errors


def test_shorten_input_serializer_rejects_original_url_field() -> None:
    serializer = ShortenInputSerializer(
        data={"original_url": "https://example.com/legacy"}
    )
    assert not serializer.is_valid()
    assert "url" in serializer.errors
