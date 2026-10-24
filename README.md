# URL Shortener API

Minimalist URL shortener REST API built with Django REST Framework.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Quick Start

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

The API will be available at `http://localhost:8000`.

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/shorten/` | Create a new short URL |
| `GET` | `/api/v1/expand/<short_code>/` | Resolve short code to original URL (JSON) |
| `GET` | `/shrt/<short_code>/` | Redirect to original URL (HTTP 302) |

## Usage Examples

### 1. Shorten a URL

```bash
curl --json '{"url":"https://example.com/very-very/long/url/even-longer"}' http://localhost:8000/api/v1/shorten/
```


**Response (`201 Created`):**
```json
{
  "short_url": "http://localhost:8000/shrt/aB3x9K/"
}
```

> Replace `aB3x9K` with the code returned by the shortening endpoint.  
> On Windows PowerShell 5.1, use `curl.exe` instead of `curl` to invoke the actual cURL executable.

### 2. Expand a Short URL

```bash
curl http://localhost:8000/api/v1/expand/aB3x9K/
```

**Response (`200 OK`):**
```json
{
  "original_url": "https://example.com/very-very/long/url/even-longer"
}
```

Returns `404 Not Found` if the code does not exist.

### 3. Redirect to Original URL

```bash
curl -i http://localhost:8000/shrt/aB3x9K/
```

**Response (`302 Found`):**
```http
HTTP/1.1 302 Found
Location: https://example.com/very-very/long/url/even-longer
```

Returns `404 Not Found` if the code does not exist.

## Tests & Code Quality

```bash
# Run unit and E2E tests
uv run pytest

# Run static type checking
uv run mypy .

# Run linter & formatter checks
uv run ruff check .
uv run ruff format --check .
```

## Assumptions

- URL expansion was not explicitly defined, so both JSON resolution and HTTP 302 redirection are supported.
- Each shortening request generates a new unique code, even for previously submitted URLs.
