from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.config import settings
from uuid import UUID


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create new user with hashed password."""
        db_obj = User(
            email=obj_in.email,
            password_hash=get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
            settings=obj_in.settings,
            subscription_tier=obj_in.subscription_tier or "free",
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """Update user."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # Hash password if it's being updated
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password_hash"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password."""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """Check if user is active."""
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """Check if user is superuser."""
        return user.is_superuser

    def get_multi_by_subscription(
        self, db: Session, *, subscription_tier: str, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """Get users by subscription tier."""
        return (
            db.query(User)
            .filter(User.subscription_tier == subscription_tier)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_subscription(
        self, db: Session, *, user_id: UUID, new_subscription: str
    ) -> Optional[User]:
        """Update user's subscription tier."""
        user = self.get(db, id=user_id)
        if not user:
            return None

        update_data = {"subscription_tier": new_subscription}
        return self.update(db, db_obj=user, obj_in=update_data)

    def update_settings(
        self, db: Session, *, user_id: UUID, settings: Dict[str, Any]
    ) -> Optional[User]:
        """Update user's settings."""
        user = self.get(db, id=user_id)
        if not user:
            return None

        # Merge existing settings with new ones
        current_settings = user.settings or {}
        current_settings.update(settings)

        update_data = {"settings": current_settings}
        return self.update(db, db_obj=user, obj_in=update_data)

    def deactivate(self, db: Session, *, user_id: UUID) -> Optional[User]:
        """Deactivate user."""
        user = self.get(db, id=user_id)
        if not user:
            return None

        update_data = {"is_active": False}
        return self.update(db, db_obj=user, obj_in=update_data)

    def change_password(
        self, db: Session, *, user_id: UUID, current_password: str, new_password: str
    ) -> Optional[User]:
        """Change user's password with verification."""
        user = self.get(db, id=user_id)
        if not user:
            return None

        if not verify_password(current_password, user.password_hash):
            return None

        update_data = {"password": new_password}
        return self.update(db, db_obj=user, obj_in=update_data)


# Create singleton instance
user = CRUDUser(User)
