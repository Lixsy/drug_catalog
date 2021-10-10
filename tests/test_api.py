from typing import List, Tuple

import pytest
from fastapi.testclient import TestClient

from api import models
from tests.conftest import db


def create_category(category: str) -> models.CategoryModel:
    db_category = models.CategoryModel(name=category)
    db.add(db_category)
    db.commit()
    return db_category


def create_drug(drug: dict) -> models.DrugModel:
    db_drug = models.DrugModel(name=drug['name'], category_id=drug['category_id'], description=drug['description'],
                               prescription=drug['prescription'], price=drug['price'])
    db.add(db_drug)
    db.commit()
    return db_drug


def get_one_drug(drug_name: str) -> models.DrugModel:
    result = db.query(models.DrugModel).filter(models.DrugModel.name == drug_name).first()
    return result


def delete_one_category(category_id: int) -> int:
    result = db.query(models.CategoryModel).filter(models.CategoryModel.id == category_id).delete()
    db.commit()
    return result


def update_one_category(category_id: int, category_name: str) -> models.CategoryModel:
    result = db.query(models.CategoryModel).filter(models.CategoryModel.id == category_id).update(
        {'name': category_name}
    )
    db.commit()
    return result


def update_one_drug(drug_id: int, drug: dict) -> models.DrugModel:
    result = db.query(models.DrugModel).filter(models.DrugModel.id == drug_id).update(
        {'name': drug['name'],
         'category_id': drug['category_id'],
         'description': drug['description'],
         'prescription': drug['prescription'],
         'price': drug['price']}
    )
    db.commit()
    return result


@pytest.mark.parametrize('categories', [('B'), ('C'), ('D')])
def test_get_categories_not_empty(client: TestClient, categories: List[Tuple[str]]):
    arr_of_categories = []
    data_to_response = {'data': arr_of_categories}
    for category in categories:
        created_category = create_category(category[0])
        responsed_dict = {'id': created_category.id, 'category_name': created_category.name}
        arr_of_categories.append(responsed_dict)
        print(responsed_dict)

    response = client.get('/categories')
    assert response.status_code == 200
    assert response.json() == data_to_response
    assert len(response.json()) == len(arr_of_categories)


def test_post_category_success(client: TestClient):
    category = {'category_name': 'A'}
    response = client.post('/categories', json=category)
    check_if_category_in_db = db.query(models.CategoryModel).first()
    assert response.status_code == 201
    assert check_if_category_in_db is not None
    assert response.json() == \
           {'data': {'id': check_if_category_in_db.id, 'category_name': check_if_category_in_db.name}}


def test_post_category_conflict(client: TestClient):
    category1 = {'category_name': 'A'}
    category2 = {'category_name': 'A'}
    response1 = client.post('/categories', json=category1)
    response2 = client.post('/categories', json=category2)
    check_category_in_db = db.query(models.CategoryModel).all()
    assert response1.status_code == 201
    assert response2.status_code == 409
    assert len(check_category_in_db) == 1
    assert response2.json() == {'details': f'Category with name {category2.get("category_name")} is already created'}


def test_get_drugs_by_category(client: TestClient):
    category = {'category_name': 'A'}
    client.post('/categories', json=category)
    arr_of_drugs = []
    data_to_response = {'data': arr_of_drugs}
    drugs = [{
        'category_id': 1,
        'name': 'Ингавирин',
        'prescription': False,
        'description': None,
        'price': 25
    },
        {
            'category_id': 1,
            'name': 'Амброксол',
            'prescription': False,
            'description': None,
            'price': 26
        }
    ]
    for drug in drugs:
        created_drug = create_drug(drug)
        responsed_dict = {'id': created_drug.id, 'name': created_drug.name, 'category_id': created_drug.category_id,
                          'prescription': created_drug.prescription,
                          'description': created_drug.description, 'price': created_drug.price}
        arr_of_drugs.append(responsed_dict)
    response = client.get('/drugs')
    check_if_drugs_in_db = db.query(models.DrugModel).all()
    assert response.status_code == 200
    assert len(check_if_drugs_in_db) == 2
    assert response.json() == data_to_response


def test_post_drug_conflict(client: TestClient):
    category = {'category_name': 'A'}
    client.post('/categories', json=category)
    drug1 = {
        'category_id': 1,
        'name': 'Ингавирин',
        'prescription': False,
        'description': None,
        'price': 25
    }
    drug2 = {
        'category_id': 1,
        'name': 'Ингавирин',
        'prescription': False,
        'description': None,
        'price': 28
    }

    response1 = client.post('/drugs', json=drug1)
    response2 = client.post('/drugs', json=drug2)
    check_category_in_db = db.query(models.CategoryModel).all()
    assert response1.status_code == 201
    assert response2.status_code == 409
    assert len(check_category_in_db) == 1
    assert response2.json() == {'details': f'Drug with name {drug2.get("name")} is already created'}


def test_post_drug_fail(client: TestClient):
    drug = {
        'category_id': 10,
        'name': 'Ибупрофен',
        'prescription': False,
        'description': None,
        'price': 220
    }
    response = client.post('/drugs', json=drug)
    check_if_drugs_in_db = db.query(models.DrugModel).all()
    assert response.status_code == 404
    assert len(check_if_drugs_in_db) == 0
    assert response.json() == {'details': 'Cannot identify category'}


def test_delete_one_category_success(client: TestClient):
    category = {'category_name': 'A'}
    client.post('/categories', json=category)
    response = client.delete('/categories/1')
    check_category_in_db = db.query(models.CategoryModel).all()
    assert response.status_code == 204
    assert len(check_category_in_db) == 0


def test_delete_one_category_fail(client: TestClient):
    category = {'category_name': 'A'}
    client.post('/categories', json=category)
    drug = {
        'category_id': 1,
        'name': 'Ингавирин',
        'prescription': False,
        'description': None,
        'price': 28
    }

    client.post('/drugs', json=drug)
    get_drugs_by_category_1 = db.query(models.DrugModel).filter(
        models.DrugModel.category_id == drug['category_id']).all()
    response = client.delete('/categories/0')
    response2 = client.delete('/categories/1')
    if len(get_drugs_by_category_1) == 0:
        assert response2.status_code == 404
        assert response2.json() == {'details': f'Firstly you need to delete drugs from category {drug["category_id"]}'}

    if response:
        check_category_in_db = db.query(models.CategoryModel).all()
        assert response.status_code == 404
        assert len(check_category_in_db) == 1
        assert response.json() == {'details': 'Category with id 0 was not found'}


def test_delete_one_drug(client: TestClient):
    category = {'category_name': 'A'}
    client.post('/categories', json=category)
    drug1 = {
        'category_id': 1,
        'name': 'Ингавирин',
        'prescription': False,
        'description': None,
        'price': 28
    }

    client.post('/drugs', json=drug1)
    response = client.delete('/drugs/2')
    response2 = client.delete('/drugs/1')
    if response:
        assert response.status_code == 404
        assert {'data': response.json()} == {'data': {'details': f'Drug with id 2 was not found'}}
    if response2:
        assert response2.status_code == 204


def test_update_category(client: TestClient):
    category = {'category_name': 'A'}
    client.post('/categories', json=category)
    new_category = {'category_name': 'B'}
    get_category_from_db = db.query(models.CategoryModel).filter(models.CategoryModel.name == 'A').first()
    update_category_in_db = update_one_category(get_category_from_db.id, new_category['category_name'])
    response = client.put('/categories/1', json=new_category)
    response2 = client.put('/categories/77', json=category)
    if response:
        assert response.status_code == 200
        assert response.json() == {'details': 'Updated successfully'}
        assert update_category_in_db == 1
    if response2:
        assert response2.status_code == 404
        assert response2.json() == {'details': 'Nothing to update'}


def test_update_drug(client: TestClient):
    category = {'category_name': 'A'}
    client.post('/categories', json=category)
    drug = {
        'category_id': 1,
        'name': 'Ингавирин',
        'prescription': False,
        'description': None,
        'price': 28
    }
    client.post('/drugs', json=drug)

    drug_to_update1 = {
        'category_id': 1,
        'name': 'Барбазол',
        'prescription': True,
        'description': 'Лечит зуд',
        'price': 28
    }
    drug_to_update2 = {
        'category_id': 88,
        'name': 'Барбазол',
        'prescription': True,
        'description': 'Лечит зуд',
        'price': 28
    }
    get_drug_from_db = get_one_drug(drug['name'])
    update_one_drug(get_drug_from_db.id, drug_to_update1)
    drugs_in_db = db.query(models.DrugModel).all()
    response1 = client.put('/drugs/1', json=drug_to_update1)

    response2 = client.put('/drugs/2', json=drug_to_update2)
    if response1:
        assert response1.status_code == 200
        assert response1.json() == {'details': 'Updated successfully'}
        assert len(drugs_in_db) == 1
    if response2:
        assert response2.status_code == 400
        assert response2.json() == {'details': 'Category was not found or drug name is already exists'}
        assert len(drugs_in_db) == 1


def test_drug_nothing_to_update(client: TestClient):
    drug = {
        'category_id': 1,
        'name': 'Ингавирин',
        'prescription': False,
        'description': None,
        'price': 28
    }
    without_drugs_in_db = db.query(models.DrugModel).filter(models.DrugModel.name == drug['name']).all()
    response = client.put('/drugs/1', json=drug)
    assert response.status_code == 404
    assert response.json() == {'details': 'Nothing to update'}
    assert len(without_drugs_in_db) == 0
