from datetime import datetime
from fastapi import Request, Depends, status
from jose import JWTError, jwt
from app.exceptions import IncorrectTokenFormatException, TokenAbsentException, TokenExpiredException, UserIsNotPresentException
from app.users.dao import UserDAO

from app.config import settings
from app.users.models import Users

def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user

async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
 #   if current_user.role != 'admin':
 #       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user