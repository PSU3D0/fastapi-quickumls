FROM python:3.9-slim-bullseye as python

FROM python as python-build-stage

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential

COPY requirements/base.txt .
COPY requirements/server.txt .

RUN pip wheel --wheel-dir /usr/src/app/wheels -r server.txt
RUN pip install -r base.txt

COPY ./umls/umls-2023AA-metathesaurus-full ./umls



RUN python -m quickumls.install umls /usr/src/app/umls -d unqlite

FROM python as python-run-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app

COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY --from=python-build-stage /usr/src/app/umls /app/umls

EXPOSE 4645