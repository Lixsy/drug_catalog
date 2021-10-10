from typing import Optional
from fastapi import FastAPI, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, Response

from api import crud
from api import models
from api import schemas
from api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/categories', response_model=schemas.ResponseCategories, status_code=200)
def get_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    schemas_arr_categories = [schemas.Category(id=model.id, category_name=model.name) for model in categories]
    return schemas.ResponseCategories(data=schemas_arr_categories)


@app.post('/categories', response_model=schemas.ResponseCategory, status_code=201)
def post_one_category(category: schemas.PostCategory, db: Session = Depends(get_db)):
    try:
        created_category = crud.create_category(db, category)
        return schemas.ResponseCategory(
            data=schemas.Category(id=created_category.id, category_name=created_category.name))
    except IntegrityError:
        return JSONResponse({'details': f'Category with name {category.category_name} is already created'},
                            status_code=409)


@app.get('/drugs', response_model=schemas.ResponseDrugs, status_code=200)
def get_all_drugs(category_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    drugs = crud.get_all_drugs(db, category_id=category_id)
    schemas_arr_drugs = [
        schemas.Drug(id=model.id, name=model.name, category_id=model.category_id, description=model.description,
                     prescription=model.prescription,
                     price=model.price) for model in drugs]
    return schemas.ResponseDrugs(data=schemas_arr_drugs)


@app.post('/drugs', response_model=schemas.PostDrug, status_code=201)
def post_one_drug(drug: schemas.PostDrug, db: Session = Depends(get_db)):
    if crud.get_category_to_check_if_it_is_in_db(db, category_id=drug.category_id):
        try:
            created_drug = crud.create_drug(db, drug)
            return schemas.Drug(id=created_drug.id, name=created_drug.name, category_id=created_drug.category_id,
                                description=created_drug.description, prescription=created_drug.prescription,
                                price=created_drug.price)
        except IntegrityError:
            return JSONResponse({'details': f'Drug with name {drug.name} is already created'}, status_code=409)
    return JSONResponse({'details': 'Cannot identify category'}, status_code=404)


@app.delete('/categories/{category_id}', status_code=204)
def delete_one_category(category_id: int, db: Session = Depends(get_db)):
    try:
        result = crud.delete_one_category(db, category_id=category_id)
    except IntegrityError:
        return JSONResponse(
            {'details': f'Firstly you need to delete drugs from category {category_id}'}, status_code=404)
    if result == 0:
        return JSONResponse({'details': f'Category with id {category_id} was not found'}, status_code=404)
    return Response(status_code=204)


@app.delete('/drugs/{drug_id}', status_code=204)
def delete_one_drug(drug_id: int, db: Session = Depends(get_db)):
    result = crud.delete_one_drug(db, drug_id=drug_id)
    if result == 0:
        return JSONResponse({'details': f'Drug with id {drug_id} was not found'}, status_code=404)
    return Response(status_code=204)


@app.put('/categories/{category_id}', response_model=schemas.ResponseUpdate, status_code=200)
def update_category_info(category_id: int, category_to_update: schemas.PostCategory, db: Session = Depends(get_db)):
    if crud.get_one_category(db, category_id=category_id):
        crud.update_one_category(db, category_id=category_id, category=category_to_update)
        return schemas.ResponseUpdate(details='Updated successfully')
    return JSONResponse({'details': 'Nothing to update'}, status_code=404)


@app.put('/drugs/{drug_id}', response_model=schemas.ResponseUpdate, status_code=200)
def update_drug_info(drug_id: int, drug_to_update: schemas.PostDrug, db: Session = Depends(get_db)):
    if crud.get_one_drug(db, drug_id=drug_id):
        try:
            crud.update_one_drug(db, drug_id=drug_id, drug=drug_to_update)
        except IntegrityError:
            return JSONResponse({'details': 'Category was not found or drug name is already exists'},
                                status_code=400)
        return schemas.ResponseUpdate(details='Updated successfully')
    return JSONResponse({'details': 'Nothing to update'}, status_code=404)
