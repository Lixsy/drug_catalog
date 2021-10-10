from typing import List

from sqlalchemy.exc import IntegrityError

from api import models
from api.database import SessionLocal

MOCK = [
    {
        'id': 1,
        'drug_name': 'Терафлю',
        'category': '1',
        'form of using': 'Перорально',
        'dosage': '140mg',
        'drug_description': 'От живота',
        'prescription': False,
        'price': '255',

    },
    {
        'id': 1,
        'drug_name': 'Линекс',
        'category': '7',
        'form of using': 'Перорально',
        'dosage': '140mg',
        'drug_description': 'От живота',
        'prescription': False,
        'price': '255',

    },
    {
        'id': 1,
        'drug_name': 'Мазь',
        'category': '47',
        'form of using': 'Перорально',
        'dosage': '140mg',
        'drug_description': 'От живота',
        'prescription': False,
        'price': '255',

    }
]

CATEGORY_MAP = {'7': 1,
                '6': 2,
                '5': 3,
                }


def request_drugs() -> List[dict]:
    return MOCK


def import_drugs():
    db = SessionLocal()
    requested_drugs = request_drugs()
    for drug in requested_drugs:
        if drug['category'] not in CATEGORY_MAP:
            print(f'Category with {drug["category"]} was not found')
            continue
        try:
            db_drug = models.DrugModel(name=drug['drug_name'], category_id=CATEGORY_MAP[drug['category']],
                                       description=drug['drug_description'],
                                       prescription=drug['prescription'], price=int(drug['price']))
            db.add(db_drug)
            db.commit()
        except IntegrityError as e:
            print(f'Cannot save this {drug} because of {e}')
    db.close()
