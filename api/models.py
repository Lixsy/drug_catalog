from api.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Numeric


class CategoryModel(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)


class DrugModel(Base):
    __tablename__ = 'drug'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    description = Column(String, nullable=False)
    prescription = Column(Boolean, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
