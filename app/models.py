from datetime import datetime

from sqlalchemy import Column, Index, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True)
    status = Column(String(20), default="неполный")
    created_at = Column(DateTime, default=datetime.utcnow)
    group_last_used = Column(DateTime, nullable=True)
    group_use_count = Column(Integer, default=0)
    superprice_last_used = Column(DateTime, nullable=True)
    superprice_use_count = Column(Integer, default=0)

    last_edited = Column(DateTime, nullable=True)

    products = relationship(
        "Product",
        back_populates="block",
        cascade="all, delete-orphan",
        order_by="Product.order",
    )


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (Index("ix_product_article", "article"),)

    id = Column(Integer, primary_key=True)
    block_id = Column(Integer, ForeignKey("blocks.id", ondelete="CASCADE"))
    photo_file_id = Column(String(512))
    text = Column(String(1024))
    article = Column(String(128))
    size = Column(String(64))
    order = Column(Integer, default=0)

    block = relationship("Block", back_populates="products")
