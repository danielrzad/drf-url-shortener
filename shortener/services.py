import secrets
import string

from django.db import IntegrityError, transaction

from shortener.models import CODE_LENGTH, ShortenedURL

BASE62_CHARACTERS: str = string.digits + string.ascii_letters
MAX_CREATION_ATTEMPTS: int = 10


def generate_random_code(length: int = CODE_LENGTH) -> str:
    return "".join(secrets.choice(BASE62_CHARACTERS) for _ in range(length))


def create_short_url(
    original_url: str,
    length: int = CODE_LENGTH,
    max_attempts: int = MAX_CREATION_ATTEMPTS,
) -> ShortenedURL:
    for _ in range(max_attempts):
        code = generate_random_code(length=length)
        try:
            with transaction.atomic():
                return ShortenedURL.objects.create(
                    original_url=original_url,
                    short_code=code,
                )
        except IntegrityError:
            continue
    raise RuntimeError("Failed to generate a unique short code after maximum attempts.")
