from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True