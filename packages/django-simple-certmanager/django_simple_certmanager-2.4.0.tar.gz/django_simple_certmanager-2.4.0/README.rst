django-simple-certmanager
=========================

:Version: 2.4.0
:Source: https://github.com/maykinmedia/django-simple-certmanager
:Keywords: certificates

|build-status| |code-quality| |black| |coverage| |docs|

|python-versions| |django-versions| |pypi-version|

Manage TLS certificates and keys in the Django admin

.. contents::

.. section-numbering::

Features
========

* Manage (mutual) TLS certificates
* Certificate introspection and validation
* Certificate/key files stored in private media
* Certificate/key files deleted when the database record is deleted


Installation
============

Requirements
------------

* Python 3.10 or above
* Django 3.2 or newer


Install
-------

You can install **Django Simple Certmanager** either via the Python Package 
Index (PyPI) or from source.

To install using ``pip``:

.. code-block:: bash

    pip install django-simple-certmanager


Usage
=====

To use this with your project you need to follow these steps:

#. Add **Django Simple Certmanager** to ``INSTALLED_APPS`` in your Django 
   project's ``settings.py``:

   .. code-block:: python

      INSTALLED_APPS = (
          # ...,
          "privates",  # Needed for admin usage.
          "simple_certmanager"
      )

#. Make sure you configure `Django Privates`_ correctly and set the (currently)
   undocumented settings:

   .. code-block:: python

      PRIVATE_MEDIA_ROOT = os.path.join(BASE_DIR, "private-media")
      PRIVATE_MEDIA_URL = "/private-media/"

#. Run the migrations

.. code-block:: bash

    python manage.py migrate


.. _`Django Privates`: https://pypi.org/project/django-privates/


.. |build-status| image:: https://github.com/maykinmedia/django-simple-certmanager/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/django-simple-certmanager/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/maykinmedia/django-simple-certmanager/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/django-simple-certmanager/actions?query=workflow%3A%22Code+quality+checks%22

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/maykinmedia/django-simple-certmanager/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/django-simple-certmanager
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/django-simple-certmanager/badge/?version=latest
    :target: https://django-simple-certmanager.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/django-simple-certmanager.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/django-simple-certmanager.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-simple-certmanager.svg
    :target: https://pypi.org/project/django-simple-certmanager/
