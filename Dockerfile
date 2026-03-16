FROM python:3.14-alpine

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==2.2.1"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY megano .
COPY diploma-frontend .

CMD ["gunicorn", "megano.wsgi:application", "--bind", "0.0.0.0:8000"]
