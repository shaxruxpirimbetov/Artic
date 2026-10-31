# Artic API

A RESTful backend for an art-sharing platform. Artists register, publish artworks, and discuss them in comments. Built with Django and Django REST Framework, secured with JWT authentication, and storing media on Cloudflare R2 (S3-compatible object storage).

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-REST%20API-A30000)
![Auth](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)
![Storage](https://img.shields.io/badge/Storage-Cloudflare%20R2-F38020?logo=cloudflare&logoColor=white)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Authentication](#authentication)
- [API Reference](#api-reference)
- [Data Model](#data-model)
- [Security](#security)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Features

- **JWT authentication** with access and refresh tokens (SimpleJWT).
- **Role-aware permissions**: public read access, authenticated writes, owner-only edits, superuser override.
- **User profiles** with avatar upload and a dedicated `/me` endpoint.
- **Artworks**: image upload, title and description validation, soft-visibility flag (`is_active`).
- **Comments** linked to artworks, editable and deletable by their author.
- **Password validation** on registration using Django's built-in validators.
- **Request throttling** for anonymous and authenticated clients.
- **Cloudflare R2 media storage** through `django-storages`, served from a public CDN domain.
- **Configurable CORS** with an explicit origin allow-list.
- **Paginated responses** (20 items per page) in JSON only.

## Tech Stack

| Layer          | Technology                                   |
| -------------- | -------------------------------------------- |
| Language       | Python 3.12+                                 |
| Framework      | Django 6.1, Django REST Framework            |
| Auth           | `djangorestframework-simplejwt`              |
| Database       | SQLite (default, swappable)                  |
| Media storage  | Cloudflare R2 via `django-storages` + `boto3`|
| Image handling | Pillow                                       |
| Config         | `python-decouple`                            |
| CORS           | `django-cors-headers`                        |

## Architecture

The project is split into three focused Django apps, each owning its models, serializers, views, and routes.

```
            ┌────────────┐
 Client ───▶│  /api/...  │  DRF views + JWT auth + throttling
            └─────┬──────┘
      ┌───────────┼────────────┐
      ▼           ▼            ▼
 apps.user     apps.art    apps.comment
 (User)        (Art)       (Comment)
      │           │            │
      └─────┬─────┴────────────┘
            ▼
     SQLite / any Django DB          Cloudflare R2 (avatars, artworks)
```

- `apps.user` holds a custom `User` model (extends `AbstractUser` with an `avatar`) and the shared permission classes.
- `apps.art` handles artworks and image uploads.
- `apps.comment` handles discussion on artworks.

---

## Getting Started

### Prerequisites

- Python 3.12 or newer
- A Cloudflare R2 bucket with an access key pair (media uploads are stored there)

### Installation

```bash
git clone <your-repository-url> artic
cd artic

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Environment

Create a `.env` file in the project root (see [Configuration](#configuration)):

```env
SECRET_KEY="change-me-to-a-long-random-string"
ALLOWED_HOSTS="localhost,127.0.0.1"
CORS_ALLOWED_ORIGINS="http://localhost:5000,http://127.0.0.1:5000"

CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_ACCESS_KEY_ID=your_access_key_id
CLOUDFLARE_SECRET_ACCESS_KEY=your_secret_access_key
CLOUDFLARE_R2_BUCKET=your_bucket_name
CLOUDFLARE_R2_PUBLIC_URL=https://pub-xxxxxxxx.r2.dev
```

Generate a strong secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

### Run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`. The Django admin is at `/admin/`.

---

## Configuration

All settings are read from environment variables (or `.env`) via `python-decouple`.

| Variable                       | Required | Description                                                        |
| ------------------------------ | :------: | ------------------------------------------------------------------ |
| `SECRET_KEY`                   |   Yes    | Django secret key. Also used to sign JWTs. Keep it private.        |
| `ALLOWED_HOSTS`                |    No    | Comma-separated list of allowed hostnames.                         |
| `CORS_ALLOWED_ORIGINS`         |   Yes    | Comma-separated list of origins allowed to call the API.           |
| `CLOUDFLARE_ACCOUNT_ID`        |   Yes    | Cloudflare account ID, used to build the R2 endpoint URL.          |
| `CLOUDFLARE_ACCESS_KEY_ID`     |   Yes    | R2 access key ID.                                                  |
| `CLOUDFLARE_SECRET_ACCESS_KEY` |   Yes    | R2 secret access key.                                              |
| `CLOUDFLARE_R2_BUCKET`         |   Yes    | R2 bucket name.                                                    |
| `CLOUDFLARE_R2_PUBLIC_URL`     |   Yes    | Public base URL of the bucket (r2.dev or a custom domain).         |

Other defaults defined in `settings.py`:

| Setting                | Value                          |
| ---------------------- | ------------------------------ |
| Access token lifetime  | 5 hours                        |
| Refresh token lifetime | 1 day                          |
| Pagination page size   | 20                             |
| Anonymous throttle     | 100 requests / minute          |
| Authenticated throttle | 1000 requests / minute         |
| Response format        | JSON only                      |

---

## Authentication

The API uses **JWT Bearer tokens**.

**1. Obtain a token pair**

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "Str0ng-pass-91"}'
```

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

**2. Call protected endpoints**

```bash
curl http://127.0.0.1:8000/api/user/me/ \
  -H "Authorization: Bearer <access-token>"
```

**3. Refresh an expired access token**

```bash
curl -X POST http://127.0.0.1:8000/api/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh-token>"}'
```

---

## API Reference

Base URL: `/api/`

### Permissions legend

| Label     | Meaning                                              |
| --------- | ---------------------------------------------------- |
| Public    | No authentication required                           |
| Auth      | Any authenticated user                               |
| Owner     | The resource owner (superusers are also allowed)     |
| Admin     | Staff users only                                     |

### Auth

| Method | Endpoint        | Access | Description                   |
| ------ | --------------- | ------ | ----------------------------- |
| POST   | `/api/token/`   | Public | Obtain access and refresh JWT |
| POST   | `/api/refresh/` | Public | Refresh the access token      |

### Users

| Method    | Endpoint           | Access | Description                              |
| --------- | ------------------ | ------ | ---------------------------------------- |
| POST      | `/api/user/`       | Public | Register a new user                      |
| GET       | `/api/user/`       | Admin  | List all users                           |
| GET       | `/api/user/me/`    | Auth   | Current user's profile                   |
| GET       | `/api/user/<id>/`  | Owner  | Retrieve a profile                       |
| PATCH/PUT | `/api/user/<id>/`  | Owner  | Update username, email, name, or avatar  |

Registration requires `username`, `password`, `avatar` and accepts `email`, `first_name`, `last_name`. Because an avatar file is required, send registration as `multipart/form-data`.

```bash
curl -X POST http://127.0.0.1:8000/api/user/ \
  -F "username=alice" \
  -F "password=Str0ng-pass-91" \
  -F "email=alice@example.com" \
  -F "avatar=@./avatar.png"
```

Use `PATCH` for partial profile updates. Password changes are not handled by the profile endpoint.

### Artworks

| Method    | Endpoint          | Access | Description                  |
| --------- | ----------------- | ------ | ---------------------------- |
| GET       | `/api/art/`       | Public | List artworks (paginated)    |
| POST      | `/api/art/`       | Auth   | Publish an artwork           |
| GET       | `/api/art/<id>/`  | Public | Retrieve an artwork          |
| PATCH/PUT | `/api/art/<id>/`  | Owner  | Update an artwork            |

```bash
curl -X POST http://127.0.0.1:8000/api/art/ \
  -H "Authorization: Bearer <access-token>" \
  -F "title=Sunset over Aral" \
  -F "description=Oil on canvas, 2026" \
  -F "image=@./sunset.png"
```

Constraints: `title` is 3 to 124 characters; `description` is 3 to 500 characters; `image` must be a valid image file. The `user` and `is_active` fields are managed by the server.

### Comments

| Method           | Endpoint             | Access | Description                  |
| ---------------- | -------------------- | ------ | ---------------------------- |
| GET              | `/api/comment/`      | Public | List comments (paginated)    |
| POST             | `/api/comment/`      | Auth   | Comment on an artwork        |
| GET              | `/api/comment/<id>/` | Public | Retrieve a comment           |
| PATCH/PUT/DELETE | `/api/comment/<id>/` | Owner  | Edit or delete a comment     |

```bash
curl -X POST http://127.0.0.1:8000/api/comment/ \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{"art": 1, "content": "Beautiful use of color!"}'
```

`content` must be at least 5 characters. Responses embed the related artwork as `art_detail` and the author as `user`.

### Pagination

List endpoints return a standard DRF page envelope:

```json
{
  "count": 42,
  "next": "http://127.0.0.1:8000/api/art/?page=2",
  "previous": null,
  "results": []
}
```

### Error format

Errors are returned as JSON with conventional HTTP status codes.

| Status | Meaning                                  |
| ------ | ---------------------------------------- |
| 400    | Validation error (details in the body)   |
| 401    | Missing or invalid credentials           |
| 403    | Authenticated but not allowed            |
| 404    | Resource not found                       |
| 429    | Rate limit exceeded                      |

---

## Data Model

```
User ──< Art ──< Comment >── User
```

| Model     | Key fields                                                                                  |
| --------- | ------------------------------------------------------------------------------------------- |
| `User`    | Django `AbstractUser` fields + `avatar` (image)                                             |
| `Art`     | `user` (FK), `title`, `description`, `image`, `is_active`, `created_at`, `updated_at`       |
| `Comment` | `user` (FK), `art` (FK), `content`, `created_at`, `updated_at`                              |

Deleting a user cascades to their artworks and comments; deleting an artwork cascades to its comments.

---

## Security

- Passwords are hashed by Django and validated against the configured password validators on registration.
- Public serializers never expose `email` or `last_login`.
- Profile updates use a dedicated serializer, so passwords and privileged fields cannot be changed through it.
- Write operations require authentication; edits and deletes are restricted to the resource owner.
- CORS is limited to an explicit origin allow-list.
- Throttling is enabled for anonymous and authenticated clients.
- `DEBUG` is disabled by default.
- Secrets and storage credentials are loaded from the environment and must never be committed. `.env` is git-ignored.

**Production checklist**

- Set a unique, random `SECRET_KEY`.
- Set `ALLOWED_HOSTS` to your real domain(s).
- Serve over HTTPS behind a reverse proxy.
- Run with a production WSGI server (for example Gunicorn) and serve admin static files (for example WhiteNoise).
- Use a production database such as PostgreSQL instead of SQLite.
- Rotate any credentials that were ever shared or exposed.

---

## Project Structure

```
Artic/
├── Artic/                 # Project config: settings, root URLs, WSGI/ASGI
├── apps/
│   ├── user/              # Custom User model, auth serializers, permissions
│   ├── art/               # Artwork model, serializers, views
│   └── comment/           # Comment model, serializers, views
├── manage.py
└── requirements.txt
```

---

## Roadmap

- [ ] Hide inactive artworks from public listings
- [ ] Optimize comment and art queries (`select_related`)
- [ ] Dedicated change-password endpoint
- [ ] Automated test suite and CI
- [ ] Docker setup and PostgreSQL support
- [ ] OpenAPI / Swagger documentation

---

## Author

Built by **Shaxrux**, backend developer at **QIT Company**, Nukus, Uzbekistan.

<!-- Add your links: GitHub, LinkedIn, e-mail -->

## License

Add a license of your choice (for example MIT) in a `LICENSE` file and reference it here.