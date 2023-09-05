from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship
from ..database import Base


class User_Accounts(Base):
    __tablename__ = "user_accounts"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    api_key = Column(String)
    password_hash = Column(String)
    disabled = Column(Boolean, default=True)
    indicators = relationship("Indicators", back_populates="creator")

    @classmethod
    def get_user_by_username(cls, username: str, db: Session):
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def get_user_by_api_key(cls, api_key: str, db: Session):
        return db.query(cls).filter(cls.api_key == api_key).first()

    @classmethod
    def get_user_by_id(cls, user_id: int, db: Session):
        return db.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def get_all_users(cls, db: Session):
        return db.query(cls).order_by(cls.id.desc()).all()
