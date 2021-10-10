from typing import List, Optional

from sqlalchemy.orm import Session

from api import models
from api import schemas


def create_category(db: Session, category: schemas.PostCategory) -> models.CategoryModel:
    db_category = models.CategoryModel(name=category.category_name)
    db.add(db_category)
    db.commit()
    return db_category


def create_drug(db: Session, drug: schemas.PostDrug) -> models.DrugModel:
    db_drug = models.DrugModel(name=drug.name, category_id=drug.category_id, description=drug.description,
                               prescription=drug.prescription, price=drug.price)
    db.add(db_drug)
    db.commit()
    return db_drug


def get_categories(db: Session) -> List[models.CategoryModel]:
    return db.query(models.CategoryModel).order_by(models.CategoryModel.id.asc()).all()


def get_all_drugs(db: Session, category_id: Optional[int]) -> List[models.DrugModel]:
    if category_id is None:
        return db.query(models.DrugModel).order_by(models.DrugModel.id.asc()).all()
    else:
        return db.query(models.DrugModel).filter(models.DrugModel.category_id == category_id).order_by(
            models.DrugModel.id.asc()).all()


def get_one_drug(db: Session, drug_id: int) -> models.DrugModel:
    result = db.query(models.DrugModel).filter(models.DrugModel.id == drug_id).first()
    return result


def get_one_category(db: Session, category_id: int) -> models.CategoryModel:
    result = db.query(models.CategoryModel).filter(models.CategoryModel.id == category_id).first()
    return result


def get_category_to_check_if_it_is_in_db(db: Session, category_id: int) -> models.CategoryModel:
    result = db.query(models.CategoryModel).filter(models.CategoryModel.id == category_id).first()
    return result


def delete_one_category(db: Session, category_id: int) -> int:
    result = db.query(models.CategoryModel).filter(models.CategoryModel.id == category_id).delete()
    db.commit()
    return result


def delete_one_drug(db: Session, drug_id: int) -> int:
    result = db.query(models.DrugModel).filter(models.DrugModel.id == drug_id).delete()
    db.commit()
    return result


def update_one_drug(db: Session, drug_id: int, drug: schemas.PostDrug) -> models.DrugModel:
    result = db.query(models.DrugModel).filter(models.DrugModel.id == drug_id).update(
        {'name': drug.name,
         'category_id': drug.category_id,
         'description': drug.description,
         'prescription': drug.prescription,
         'price': drug.price}
    )
    db.commit()
    return result


def update_one_category(db: Session, category_id: int, category: schemas.PostCategory) -> models.CategoryModel:
    result = db.query(models.CategoryModel).filter(models.CategoryModel.id == category_id).update(
        {'name': category.category_name}
    )
    db.commit()
    return result
