FROM python:3.10-slim

WORKDIR /app

RUN pip install "poetry==1.3.2"

# copy poetry metadata
COPY rubertconv_toxic_clf/ rubertconv_toxic_clf/
COPY poetry.lock .
COPY pyproject.toml .
COPY server.py .

RUN poetry config virtualenvs.create false && \
    poetry install --only server

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

ENTRYPOINT [ "python3" ]

CMD [ "server.py" ]