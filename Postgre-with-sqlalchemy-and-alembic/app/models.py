from sqlalchemy import Column,Integer,String,UniqueConstraint,DateTime,Boolean
from app.database import Base
from sqlalchemy.sql import func
class User(Base):
    __tablename__="users"
    id=Column(
        Integer,
        primary_key=True,
        index=True,
        nullable=False
    )
    email=Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )
    username=Column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    created_at=Column(
        DateTime(timezone=True),server_default=func.now(),nullable=False
    )
    is_active=Column(Boolean,default=True,nullable=False)

    __table_args__=(
        UniqueConstraint("email",name="uq_usersh_email"),
        UniqueConstraint("username",name="uq_usersh_username"),
    )

    def __repr__(self):
        """String representation of User object"""
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"

        