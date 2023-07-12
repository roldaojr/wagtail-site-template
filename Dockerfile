FROM python:3.10-slim as base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000
EXPOSE 8000
LABEL name="project_name"
LABEL description="Wagtail CodeRed CMS website"
ENV BUILD_DEPS="git"

RUN useradd wagtail
RUN mkdir /app
WORKDIR /app
ADD Pipfile.lock /app/
ADD Pipfile /app/
RUN apt-get update && apt install -y --no-install-recommends $BUILD_DEPS \
    && python3 -m pip install --upgrade pip setuptools wheel \
    && pip3 install --no-cache-dir pipenv \
    && pipenv install --system --deploy --clear \
    && apt-get remove --purge -y $BUILD_PACKAGES \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
FROM base as app
COPY . /app/
RUN python manage.py compilescss
CMD gunicorn

FROM app as app-with-static
RUN python manage.py collectstatic --ignore=*.scss --noinput
