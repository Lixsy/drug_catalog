export PYTHONPATH="${PYTHONPATH}:."
export pg_user=test
export pg_pass=test
export pg_host=localhost
export pg_port=5432
export pg_db=drug_catalog
python3 scripts/import_drugs.py