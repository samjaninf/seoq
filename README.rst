SEO Quotient
==============================

Version 0.1.1

Is an online community that provides information, education, and tools for website owners, search engine optimization (SEO) professionals, digital marketing professionals, and students aspiring to enhance their careers in SEO and digital marketing.


.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django



Settings
------------

Project requires some Settings. They can be configured at .env file.

::

	BALYSTIC_API_TOKEN=YOUR_API_TOKEN
	BALYSTIC_API_PATH=http://BALYSTIC_URL/api/


Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test


Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  $ npm install
  $ bower install
  $ gulp watch


Windows Configuration
^^^^^^^^^^^^^^^^^^^^^

You can use Vagrant or Docker.

Vagrant

::

    vagrant up
    # This will download an ubuntu box, which could take a little
    # After you are done with that, you can go into the box with:
    vagrant ssh
    # Install ansible with:
    sudo apt-get update
    sudo apt-get install python-pip libffi-dev libssl-dev python-dev
    sudo pip install ansible==2.0.2
    sudo pip install setuptools==11.3
    # Now you run the playbook to setup your django project:
    cd /vagrant/
    ansible-playbook playbook.yml
    # Once you have the instance running, you need to activate the virtualenv:
    source /home/vagrant/.envs/seoq/bin/activate
    # To run the server, run:
    cd /vagrant
    python manage.py runserver 0.0.0.0:9000
    # Then on windows, go to http://localhost:9000 and you are ready to go.
    # If you want to connect directly to the postgres instance, it is in the port 5433.
    
    # In some cases, the ansible playbook is failing in the last step (Sync DB).
    # In that case, you need to migrate manually:
    python manage.py migrate

Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://getsentry.com/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.
