===============================
Packr
===============================

.. image:: https://badge.waffle.io/KnightHawk3/packr.png?label=ready&title=Ready 
 :target: https://waffle.io/KnightHawk3/packr
 :alt: 'Stories in Ready'

.. image:: https://travis-ci.org/KnightHawk3/packr.svg?branch=master
  :target: https://travis-ci.org/KnightHawk3/packr
  :alt: 'Build status'

For package management


Quickstart
----------

First, set your app's secret key as an environment variable. For example, example add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export PACKR_SECRET='something-really-secret'


Then run the following commands to bootstrap your environment.


::

    git clone https://github.com/KnightHawk3/packr
    cd packr
    vagrant up
    vagrant ssh
    cd packr
    python manage.py runserver -p 80 -h 0.0.0.0

You will see a pretty welcome screen at 192.168.33.11, this ip is only accessible from your computer (its virtual and stuff).
You can also modify the files in the packr folder on your local computer and it will be mirrored across to the virtual machine instantly (its a network store technically)

These commands are to make your database work if its broken, probably dont need this unless you know what your doing.

::

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``PACKR_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
