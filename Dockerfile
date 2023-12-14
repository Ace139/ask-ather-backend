FROM python:3.11-buster

WORKDIR /app

COPY . .

RUN pip install wheel
RUN pip install poetry
RUN poetry install

EXPOSE 8000

ENTRYPOINT [ "python3", "main.py" ]
