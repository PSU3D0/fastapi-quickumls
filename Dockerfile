FROM python:3.9-slim-bullseye as python

FROM python as umls-build-stage

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential

COPY requirements/base.txt .

RUN pip install -r base.txt

COPY ./umls/umls-2023AA-metathesaurus-full ./umls

RUN mkdir -p /usr/src/app/umls

RUN python -m quickumls.install umls/2023AA/META /usr/src/app/umls -d unqlite


FROM python as python-build-stage

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential

COPY requirements/base.txt .
COPY requirements/server.txt .

RUN pip wheel --wheel-dir /usr/src/app/wheels -r server.txt

FROM python as python-run-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app

COPY --from=umls-build-stage /usr/src/app/umls /app/umls

COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

RUN python -m spacy download en_core_web_sm

WORKDIR /app/code

COPY src/ .

EXPOSE 4645
