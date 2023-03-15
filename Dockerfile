FROM python:3.10-alpine

WORKDIR /app

# installing poetry
RUN pip install "poetry==1.3.2"

# copy poetry metadata
COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false && \
    poetry install

COPY handlers/ handlers/
COPY config.py .
COPY main.py .

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]