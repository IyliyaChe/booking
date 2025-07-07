from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

""" class Users(Base):
    __tablename__ = 'users'
    id= Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False) """

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    booking = relationship("Bookings", back_populates="user")

    def __str__(self):
        return f"User #{self.email}"
    