import hashlib
import hmac
import json
import secrets
from pathlib import Path
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel, Field

USERS_DDBB_PATH = Path(__file__).resolve().parent.parent / "ddbb" / "users_ddbb.json"
_PBKDF2_ITERATIONS = 100_000


class UserPublic(BaseModel):
    """Public user/client view without sensitive credentials."""

    id: int
    name: str
    email: str
    phone: str | None = None
    avatar: str | None = None
    is_active: bool = True


class UserRecord(UserPublic):
    """Stored user/client record including hashed password."""

    password_hash: str


class UserRegister(BaseModel):
    """Mobile registration payload."""

    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=4)
    phone: str | None = None
    avatar: str | None = None


class UserLogin(BaseModel):
    """Mobile login payload."""

    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=1)


class UserProfileUpdate(BaseModel):
    """Mobile profile update payload (basic data and avatar)."""

    name: str | None = Field(default=None, min_length=1)
    email: str | None = Field(default=None, min_length=3)
    phone: str | None = None
    avatar: str | None = None


class PasswordChange(BaseModel):
    """Mobile password change payload."""

    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=4)


class ClientCreate(BaseModel):
    """Desktop admin client creation payload."""

    id: int | None = None
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    password: str = Field(default="changeme123", min_length=4)
    phone: str | None = None
    avatar: str | None = None
    is_active: bool = True


class ClientUpdate(BaseModel):
    """Desktop admin client update payload."""

    name: str | None = Field(default=None, min_length=1)
    email: str | None = Field(default=None, min_length=3)
    phone: str | None = None
    avatar: str | None = None
    is_active: bool | None = None


def hash_password(password: str) -> str:
    """Hash a plaintext password using salted PBKDF2-HMAC-SHA256."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        _PBKDF2_ITERATIONS,
    ).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a plaintext password against a stored salt$digest hash."""
    if "$" not in stored_hash:
        return False
    salt, expected_digest = stored_hash.split("$", 1)
    actual_digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        _PBKDF2_ITERATIONS,
    ).hex()
    return hmac.compare_digest(actual_digest, expected_digest)


def to_public(user: UserRecord) -> UserPublic:
    """Strip credential fields before returning user data."""
    return UserPublic(**user.model_dump(exclude={"password_hash"}))


def read_users() -> list[UserRecord]:
    """Load all users/clients from ddbb/users_ddbb.json."""
    if not USERS_DDBB_PATH.exists():
        return []
    content = USERS_DDBB_PATH.read_text(encoding="utf-8").strip()
    if not content:
        return []
    data = json.loads(content)
    return [UserRecord.model_validate(item) for item in data.get("users", [])]


def write_users(users: list[UserRecord]) -> None:
    """Persist all users/clients to ddbb/users_ddbb.json."""
    USERS_DDBB_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"users": [user.model_dump() for user in users]}
    USERS_DDBB_PATH.write_text(
        json.dumps(payload, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def find_user_by_id(user_id: int) -> UserRecord | None:
    """Find a user/client by numeric ID."""
    for user in read_users():
        if user.id == user_id:
            return user
    return None


def find_user_by_email(email: str) -> UserRecord | None:
    """Find a user/client by case-insensitive email."""
    normalized = email.strip().lower()
    for user in read_users():
        if user.email.strip().lower() == normalized:
            return user
    return None


def get_user_or_404(user_id: int) -> UserRecord:
    """Return a user by ID or raise 404 Not Found."""
    user = find_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user_record(
    *,
    name: str,
    email: str,
    password: str,
    phone: str | None = None,
    avatar: str | None = None,
    is_active: bool = True,
    explicit_id: int | None = None,
) -> UserRecord:
    """Create and persist a new user/client after uniqueness checks."""
    users = read_users()
    normalized_email = email.strip().lower()

    if any(u.email.strip().lower() == normalized_email for u in users):
        raise HTTPException(status_code=409, detail="Email already registered")

    if explicit_id is not None:
        if any(u.id == explicit_id for u in users):
            raise HTTPException(status_code=409, detail="User ID already exists")
        new_id = explicit_id
    else:
        new_id = max((u.id for u in users), default=0) + 1

    record = UserRecord(
        id=new_id,
        name=name.strip(),
        email=normalized_email,
        phone=phone,
        avatar=avatar,
        is_active=is_active,
        password_hash=hash_password(password),
    )
    users.append(record)
    write_users(users)
    return record


def update_user_record(user_id: int, updates: dict[str, Any]) -> UserRecord:
    """Apply partial updates to an existing user/client."""
    users = read_users()
    target_index = next((i for i, u in enumerate(users) if u.id == user_id), None)
    if target_index is None:
        raise HTTPException(status_code=404, detail="User not found")

    current = users[target_index]
    non_nullable = {"name", "email", "is_active", "password_hash"}
    for field in non_nullable:
        if field in updates and updates[field] is None:
            raise HTTPException(status_code=400, detail=f"Field '{field}' cannot be null")
    cleaned = dict(updates)

    if "email" in cleaned:
        new_email = cleaned["email"].strip().lower()
        if any(
            u.id != user_id and u.email.strip().lower() == new_email
            for u in users
        ):
            raise HTTPException(status_code=409, detail="Email already registered")
        cleaned["email"] = new_email

    if "name" in cleaned:
        cleaned["name"] = cleaned["name"].strip()

    updated = current.model_copy(update=cleaned)
    users[target_index] = updated
    write_users(users)
    return updated


def delete_user_record(user_id: int) -> UserRecord:
    """Delete an existing user/client by ID or raise 404."""
    users = read_users()
    target = next((u for u in users if u.id == user_id), None)
    if target is None:
        raise HTTPException(status_code=404, detail="User not found")

    remaining = [u for u in users if u.id != user_id]
    write_users(remaining)
    return target
