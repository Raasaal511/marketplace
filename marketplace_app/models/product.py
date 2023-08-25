import sys

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

sys.path = ['', '..'] + sys.path[1:]

from marketplace_app.database import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    description: Mapped[bool] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    owner: Mapped['User'] = relationship('User', back_populates='product')
