# API Versioning Strategies

## Overview

API versioning allows you to evolve your API while maintaining backward compatibility for existing consumers. Choosing the right strategy depends on your API's audience, deployment model, and how frequently you expect breaking changes.

---

## 1. URL Path Versioning

The version is embedded directly in the URL path. This is the most common and visible approach.

```
# Structure
/api/v{major}/resource
```

### Examples

```
# ✅ Good: Clear version prefix
GET /api/v1/users
GET /api/v2/users
POST /api/v1/orders

# ✅ Good: Version scoped to API root
GET /api/v1/users/123/orders
GET /api/v2/users/123/orders

# ❌ Bad: Version buried in the path
GET /api/users/v1/123
GET /users/api/v2

# ❌ Bad: Using minor or patch versions in URL
GET /api/v1.2.3/users
GET /api/v1.1/users

# ❌ Bad: Mixing versioned and unversioned endpoints
GET /api/v1/users
GET /api/orders  (no version)
```

### Implementation (FastAPI)

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

# Version 1 router
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/users")
async def list_users_v1():
    return {"version": 1, "users": [...]}

# Version 2 router
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/users")
async def list_users_v2():
    # v2 returns a different response structure
    return {"version": 2, "data": {"users": [...]}, "meta": {...}}

app.include_router(v1_router)
app.include_router(v2_router)
```

**Pros:** Easy to understand, easy to route, visible in browser, cacheable by URL
**Cons:** Multiple URLs for the same resource, clients must update URLs to upgrade

---

## 2. Header Versioning

The version is specified in a custom request header, keeping URLs clean.

### Examples

```
# ✅ Good: Custom version header
GET /api/users HTTP/1.1
Host: api.example.com
Accept-Version: v1

# ✅ Good: Vendor media type with version
GET /api/users HTTP/1.1
Host: api.example.com
Accept: application/vnd.example.v2+json

# ✅ Good: Custom header with numeric version
GET /api/users HTTP/1.1
Host: api.example.com
X-API-Version: 2

# ❌ Bad: Non-standard or ambiguous header name
GET /api/users HTTP/1.1
Version: 2

# ❌ Bad: Omitting fallback behavior when header is missing
GET /api/users HTTP/1.1
# No version header — server returns 500 instead of defaulting or returning 400
```

### Implementation (FastAPI)

```python
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/api/users")
async def list_users(accept_version: str = Header("v1", alias="Accept-Version")):
    if accept_version == "v1":
        return {"users": [...]}
    elif accept_version == "v2":
        return {"data": {"users": [...]}, "meta": {...}}
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported API version: {accept_version}. Supported: v1, v2"
        )
```

**Pros:** Clean URLs, same resource URL across versions, follows HTTP semantics
**Cons:** Less visible and harder to test in browser, requires client to set headers

---

## 3. Query Parameter Versioning

The version is passed as a query parameter.

### Examples

```
# ✅ Good: Version as query parameter
GET /api/users?version=1
GET /api/users?version=2
GET /api/users/123?version=1

# ✅ Good: With other query parameters
GET /api/users?version=2&page=1&page_size=20

# ❌ Bad: Optional version with no default behavior documented
GET /api/users
# Does this return v1? Latest? Error?

# ❌ Bad: Non-numeric or inconsistent format
GET /api/users?version=latest
GET /api/users?ver=1
GET /api/users?v=2
```

### Implementation (FastAPI)

```python
from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

SUPPORTED_VERSIONS = {1, 2}
DEFAULT_VERSION = 2

@app.get("/api/users")
async def list_users(version: int = Query(DEFAULT_VERSION, ge=1)):
    if version not in SUPPORTED_VERSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported API version: {version}. Supported: {sorted(SUPPORTED_VERSIONS)}"
        )

    if version == 1:
        return {"users": [...]}
    elif version == 2:
        return {"data": {"users": [...]}, "meta": {...}}
```

**Pros:** Easy to test, easy to switch versions, visible in URL
**Cons:** Can be forgotten by clients, mixes versioning with other parameters, caching complexity

---

## 4. Content Negotiation Versioning

Uses the `Accept` header with a vendor-specific media type. This is the most RESTful approach.

### Examples

```
# ✅ Good: Vendor media type
GET /api/users HTTP/1.1
Accept: application/vnd.example.v1+json

# ✅ Good: Media type with version parameter
GET /api/users HTTP/1.1
Accept: application/json; version=2

# ✅ Good: Response includes Content-Type with version
HTTP/1.1 200 OK
Content-Type: application/vnd.example.v2+json

# ❌ Bad: Using generic Accept header for versioning
GET /api/users HTTP/1.1
Accept: application/json-v2

# ❌ Bad: Mixing media type versions in a single request
GET /api/users HTTP/1.1
Accept: application/vnd.example.v1+json, application/vnd.example.v2+json
```

### Implementation (FastAPI)

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import re

app = FastAPI()

def extract_version(accept_header: str) -> int:
    """Extract version from Accept header: application/vnd.example.v{N}+json"""
    match = re.search(r"application/vnd\.example\.v(\d+)\+json", accept_header)
    if match:
        return int(match.group(1))
    return 1  # Default to v1

@app.get("/api/users")
async def list_users(request: Request):
    accept = request.headers.get("accept", "")
    version = extract_version(accept)

    if version == 1:
        data = {"users": [...]}
    elif version == 2:
        data = {"data": {"users": [...]}, "meta": {...}}
    else:
        raise HTTPException(status_code=406, detail="Unsupported API version")

    return JSONResponse(
        content=data,
        media_type=f"application/vnd.example.v{version}+json"
    )
```

**Pros:** Most RESTful, leverages HTTP content negotiation, clean URLs
**Cons:** Complex to implement, hard to test in browser, less discoverable

---

## Comparison Table

| Strategy              | Visibility | Ease of Use | Cacheability | RESTfulness | Browser Testing |
|-----------------------|------------|-------------|--------------|-------------|-----------------|
| URL Path              | High       | High        | Excellent    | Medium      | Easy            |
| Header                | Low        | Medium      | Good         | High        | Hard            |
| Query Parameter       | Medium     | High        | Moderate     | Low         | Easy            |
| Content Negotiation   | Low        | Low         | Good         | Excellent   | Hard            |

### When to Use Each

- **URL Path**: Public APIs, third-party integrations, microservices
- **Header**: Internal APIs, APIs with few consumers you can coordinate with
- **Query Parameter**: Simple APIs, prototyping, APIs where backward compatibility is critical
- **Content Negotiation**: APIs that strictly follow REST principles, enterprise APIs

---

## 5. Breaking vs Non-Breaking Changes

Understanding what constitutes a breaking change determines when you need a new version.

### Non-Breaking Changes (No Version Bump Required)

```
# Adding a new optional field to a response
# Before
{"id": "123", "name": "Alice"}

# After — existing clients ignore the new field
{"id": "123", "name": "Alice", "avatar_url": "https://..."}
```

```
# Adding a new optional query parameter
# Before
GET /api/users?status=active

# After — existing calls still work
GET /api/users?status=active&role=admin
```

```
# Adding a new endpoint
POST /api/users/export    # New endpoint, does not affect existing ones
```

```
# Adding a new enum value (when clients handle unknown values gracefully)
# Before: status can be "active" or "inactive"
# After:  status can be "active", "inactive", or "suspended"
```

### Breaking Changes (Version Bump Required)

```
# ❌ Removing a field from a response
# v1: {"id": "123", "name": "Alice", "email": "alice@example.com"}
# v2: {"id": "123", "name": "Alice"}  — email removed

# ❌ Renaming a field
# v1: {"user_name": "Alice"}
# v2: {"username": "Alice"}

# ❌ Changing a field's type
# v1: {"id": 123}       (number)
# v2: {"id": "123"}     (string)

# ❌ Changing URL structure
# v1: GET /api/users/{id}/orders
# v2: GET /api/orders?user_id={id}

# ❌ Making an optional parameter required
# v1: POST /api/users  body: {"name": "Alice"}
# v2: POST /api/users  body: {"name": "Alice", "email": "required@now.com"}

# ❌ Changing the meaning of a status code
# v1: DELETE /api/users/123 → 200 OK with body
# v2: DELETE /api/users/123 → 204 No Content

# ❌ Changing authentication mechanism
# v1: X-API-Key: abc123
# v2: Authorization: Bearer token123
```

---

## 6. Migration and Deprecation Strategies

### Deprecation Timeline

```
Phase 1: Announce Deprecation
  - Add Sunset header to v1 responses
  - Document deprecation in changelog and API docs
  - Notify consumers via email/webhook/dashboard

Phase 2: Deprecation Period (6-12 months minimum for public APIs)
  - v1 continues to work but returns deprecation warnings
  - v2 is the recommended version
  - Monitor v1 usage and contact remaining consumers

Phase 3: End of Life
  - v1 returns 410 Gone with migration instructions
  - Redirect documentation to v2
```

### Sunset Header (RFC 8594)

The `Sunset` header indicates when an API version will be decommissioned.

```
# ✅ Good: Sunset header with deprecation link
HTTP/1.1 200 OK
Sunset: Sat, 01 Mar 2025 00:00:00 GMT
Deprecation: true
Link: <https://api.example.com/docs/migration-v1-to-v2>; rel="sunset"

# ✅ Good: Include in all responses for deprecated version
GET /api/v1/users HTTP/1.1

HTTP/1.1 200 OK
Sunset: Sat, 01 Mar 2025 00:00:00 GMT
X-API-Warn: "v1 is deprecated. Migrate to v2 by 2025-03-01. See https://api.example.com/docs/migration"
Content-Type: application/json

{"users": [...]}
```

### Implementation (FastAPI)

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

DEPRECATED_VERSIONS = {
    "v1": {
        "sunset": "Sat, 01 Mar 2025 00:00:00 GMT",
        "migration_url": "https://api.example.com/docs/migration-v1-to-v2"
    }
}

@app.middleware("http")
async def add_deprecation_headers(request: Request, call_next):
    response = await call_next(request)

    # Extract version from path
    path = request.url.path
    for version, info in DEPRECATED_VERSIONS.items():
        if f"/api/{version}/" in path:
            response.headers["Sunset"] = info["sunset"]
            response.headers["Deprecation"] = "true"
            response.headers["Link"] = f'<{info["migration_url"]}>; rel="sunset"'
            response.headers["X-API-Warn"] = (
                f"{version} is deprecated. See {info['migration_url']}"
            )
            break

    return response
```

### Version Lifecycle Status Responses

```
# Active version
GET /api/v2/users → 200 OK

# Deprecated version (still works, with warnings)
GET /api/v1/users → 200 OK
  Sunset: Sat, 01 Mar 2025 00:00:00 GMT
  Deprecation: true

# Retired version (no longer available)
GET /api/v0/users → 410 Gone
  {
    "error": "VersionRetired",
    "message": "API v0 has been retired as of 2024-01-01",
    "migration_guide": "https://api.example.com/docs/migration-v0-to-v1",
    "current_version": "v2"
  }
```

---

## 7. Multi-Version Maintenance Patterns

### Shared Business Logic

```python
# ✅ Good: Shared service layer, version-specific serializers

# services/user_service.py (version-agnostic)
class UserService:
    async def get_user(self, user_id: str) -> User:
        return await self.repository.find_by_id(user_id)

# api/v1/serializers.py
def serialize_user_v1(user: User) -> dict:
    return {"id": user.id, "name": user.name, "email": user.email}

# api/v2/serializers.py
def serialize_user_v2(user: User) -> dict:
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email_addresses": user.emails,
        "created_at": user.created_at.isoformat()
    }
```

### Router Organization

```python
# ✅ Good: Organized router structure
# api/
#   v1/
#     __init__.py
#     users.py
#     orders.py
#   v2/
#     __init__.py
#     users.py
#     orders.py

from api.v1 import router as v1_router
from api.v2 import router as v2_router

app.include_router(v1_router, prefix="/api/v1", tags=["v1"])
app.include_router(v2_router, prefix="/api/v2", tags=["v2"])
```

---

## Quick Reference

| Decision | Recommendation |
|----------|---------------|
| **Default strategy for public APIs** | URL path versioning (`/api/v1/`) |
| **Default strategy for internal APIs** | Header versioning (`Accept-Version`) |
| **Version format** | Major version only (`v1`, `v2`) |
| **Default version when unspecified** | Latest stable or return `400 Bad Request` |
| **Deprecation notice period** | 6-12 months minimum for public APIs |
| **Sunset header** | Always include on deprecated versions |
| **Breaking change** | Removing/renaming fields, changing types, changing URL structure |
| **Non-breaking change** | Adding optional fields, new endpoints, new optional parameters |
| **Max concurrent versions** | 2-3 (current + 1-2 deprecated) |
| **Retired version response** | `410 Gone` with migration guide link |
| **Migration documentation** | Provide per-version migration guides with before/after examples |
