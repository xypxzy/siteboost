import logging
from sqlalchemy.orm import Session
from app.db import base  # noqa: F401
from app.core.config import settings

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables uncommenting the next line
    # Base.metadata.create_all(bind=engine)

    # Create first superuser if it doesn't exist
    from app.crud.crud_user import user
    from app.schemas.user import UserCreate

    superuser = user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not superuser:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        superuser = user.create(db, obj_in=user_in)
        logger.info("Created first superuser")
