from sqlalchemy import String, Integer, DateTime, Text,ForeignKey
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped,relationship

class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = 'documents'

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    file_name:Mapped[str] = mapped_column(String)
    upload_date:Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
    content:Mapped[str] = mapped_column(Text)
    document_chunks:Mapped[list["DocumentChunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan"
    )

class DocumentChunk(Base):
    __tablename__ = 'document_chunks'

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    document_id:Mapped[int] = mapped_column(ForeignKey("documents.id"))
    chunk_text:Mapped[str] = mapped_column(Text)
    document:Mapped["Document"] = relationship(
        back_populates="document_chunks"
    )