from rest_framework import serializers


class ShortenInputSerializer(serializers.Serializer[dict[str, str]]):
    url = serializers.URLField(max_length=2048)
