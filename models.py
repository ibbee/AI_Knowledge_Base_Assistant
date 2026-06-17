from sqlalchemy import String, Integer, DateTime, Text
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped

class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = 'documents'

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    file_name:Mapped[str] = mapped_column(String)
    upload_date:Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
    content:Mapped[str] = mapped_column(Text)