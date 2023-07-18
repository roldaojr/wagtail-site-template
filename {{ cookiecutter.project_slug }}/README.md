# {{ cookiecutter.project_name }}

## Getting started

Make sure a recent version of Python is installed on your system.
Open this directory in a command prompt, then:

Install the software:

    pipenv install

Create database

    pipenv run manage migrate

Run the development server:

    pipenv run server

Go to http://localhost:8000/ in your browser, or http://localhost:8000/admin/ to log in and get to work!


# Copy website data

Dump data

    python manage.py dumpdata --natural-foreign --indent 2 \
        -e contenttypes -e auth.permission -e postgres_search.indexentry \
        -e wagtailcore.groupcollectionpermission \
        -e wagtailcore.grouppagepermission -e wagtailimages.rendition \
        -e sessions > data.json

You can also exclude -e wagtailcore.pagerevision to make your data.json clean
(it would only contains the latest version), but you need to edit data.json after dumpdata

    "latest_revision_created_at": null,
    "live_revision": null

Load data on new site

    python manage.py loaddata data.json


## Documentation links

* To customize the content, design, and features of the site see Wagtail CRX](https://docs.coderedcorp.com/wagtail-crx/).
* For deeper customization of backend code see [Wagtail](http://docs.wagtail.io/) and [Django](https://docs.djangoproject.com/).
* For HTML template design see [Bootstrap](https://getbootstrap.com/).

---

Made with ♥ using [Wagtail](https://wagtail.io/) + [CodeRed Extensions](https://www.coderedcorp.com/cms/)
