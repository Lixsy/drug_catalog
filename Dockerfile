FROM python:3.9

RUN pip install poetry

ENV PYTHONPATH="${PYTHONPATH}:/app"

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt
RUN pip list

COPY api /app/api
COPY scripts /app

CMD ["./gunicorn_run.sh"]