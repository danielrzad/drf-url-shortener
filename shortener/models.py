from django.db import models

CODE_LENGTH: int = 6


class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=CODE_LENGTH, unique=True)

    def __str__(self) -> str:
        return f"{self.short_code} -> {self.original_url}"
