"""Routes HTTP du module users."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import require_admin
from app.modules.users import service
from app.modules.users.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Cree un utilisateur. Cette route est reservee aux administrateurs."""
    user = service.create_user(db, user_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ce nom d'utilisateur existe deja",
        )
    return user
