from pydantic import BaseModel, EmailStr, ConfigDict


class SUserAuth(BaseModel):
    email: EmailStr
    hashed_password: str