# {{ cookiecutter.project_name }}

## Getting started

Make sure a recent version of Python is installed on your system.
Open this directory in a command prompt, then:

Intall poetry package manager

    pip install poetry

Install the dependencies:

    poetry install

Create database

    poetry run python manage.py migrate

Create the superuser:

    poetry run python manage.py createsuperuser

Run the development server:

    poetry run python manage.py runserver

Go to http://localhost:8000/ in your browser, or http://localhost:8000/admin/ to log in and get to work!

## Documentation links

-   To customize the content, design, and features of the site see
    [Wagtail CRX](https://docs.coderedcorp.com/wagtail-crx/).

-   For deeper customization of backend code see
    [Wagtail](http://docs.wagtail.io/) and
    [Django](https://docs.djangoproject.com/).

-   For HTML template design see [Bootstrap](https://getbootstrap.com/).

## Backup site data

Clear non content data

    python manage.py purge_embeds
    python manage.py purge_revisions
    python manage.py clear_wagtail_cache

Dump website data

    poetry run python -Xutf8 manage.py dumpdata --all --natural-primary --natural-foreign --indent 2 -e contenttypes -e auth.permission -e wagtailsearch.indexentry -e wagtailcore.groupcollectionpermission -e wagtailcore.grouppagepermission -e wagtailimages.rendition -e sessions > website/fixtures/website.json
    poetry run python manage.py mediabackup

# Restore site data

Clear cache

    python manage.py clear_wagtail_cache

Load data and media files

    poetry run python manage.py loaddata data.json
    poetry run python manage.py mediarestore

Update image renditions

    python manage.py wagtail_update_image_renditions

---

Made with ♥ using [Wagtail](https://wagtail.io/) +
[CodeRed Extensions](https://www.coderedcorp.com/cms/)
