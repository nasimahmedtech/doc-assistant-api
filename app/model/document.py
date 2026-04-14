from sqlalchemy import String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.db.base import Base
from datetime import datetime


class Document(Base):
    __tablename__ = "documents"
    
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    title: Mapped[str] = mapped_column(String,nullable=False)
    content: Mapped[str] = mapped_column(Text,nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    update_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),onupdate=func.now(),nullable=True)
    chunks: Mapped[list["Chunk"]] = relationship("Chunk",back_populates="document",cascade="all, delete-orphan")





class Chunk(Base):
    __tablename__ = "chunks"
    
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    document_id: Mapped[int] = mapped_column(Integer,ForeignKey("documents.id"),nullable=False)
    content: Mapped[str] = mapped_column(Text,nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer,nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(384),nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    document: Mapped["Document"] = relationship("Document",back_populates="chunks")


    






