from fastapi import FastAPI, HTTPException

from models.user import (
    PasswordChange,
    UserLogin,
    UserProfileUpdate,
    UserPublic,
    UserRegister,
    create_user_record,
    find_user_by_email,
    get_user_or_404,
    hash_password,
    to_public,
    update_user_record,
    verify_password,
)

app = FastAPI(title="VinylLab Mobile - Users API")


@app.get("/")
def introduction() -> dict[str, str]:
    """Health check endpoint for Mobile Users API."""
    return {"message": "VinylLab Mobile Users API"}


@app.post("/users/register", status_code=201, response_model=UserPublic)
def register_user(payload: UserRegister) -> UserPublic:
    """Register a new mobile user account."""
    record = create_user_record(
        name=payload.name,
        email=payload.email,
        password=payload.password,
        phone=payload.phone,
        avatar=payload.avatar,
    )
    return to_public(record)


@app.post("/users/login")
def login_user(payload: UserLogin) -> dict[str, object]:
    """Authenticate a mobile user with email and password."""
    user = find_user_by_email(payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="User account is inactive")
    return {"message": "Login successful", "user": to_public(user)}


@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int) -> UserPublic:
    """Get a mobile user's profile by ID."""
    return to_public(get_user_or_404(user_id))


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user_profile(user_id: int, payload: UserProfileUpdate) -> UserPublic:
    """Update a mobile user's basic profile data and avatar."""
    updated = update_user_record(user_id, payload.model_dump(exclude_unset=True))
    return to_public(updated)


@app.put("/users/{user_id}/password")
def change_password(user_id: int, payload: PasswordChange) -> dict[str, str]:
    """Change a mobile user's password after verifying the current password."""
    user = get_user_or_404(user_id)
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    if payload.current_password == payload.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from the current password",
        )
    update_user_record(user_id, {"password_hash": hash_password(payload.new_password)})
    return {"message": "Password updated successfully"}
