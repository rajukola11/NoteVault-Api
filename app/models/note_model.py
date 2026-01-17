from app.db.session import Base
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class NoteModel(Base):
    __tablename__ = "notevault"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=True)
    content = Column(String,nullable=True)
    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    owner = relationship("UserModel",backref="notes")

