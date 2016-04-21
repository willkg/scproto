=======
scproto
=======

This repo holds some prototyping I fiddled with for the new Socorro
collector.

It's released under the MPLv2.


What's here
===========

It contains two scripts:

* ``run_gunicorn.sh``: Runs gunicorn with the specified framework.
* ``run_siege.sh``: The siege thing I was running.

It has rough sketches of a collector implemented with:

* `bottle <http://bottlepy.org/docs/dev/index.html>`_
* `flask <http://flask.pocoo.org/>`_
* `falcon <http://falconframework.org/>`_


Setup
=====

::

    mkvirtualenv scproto
    pip install -e .


Running things
==============

::

    ./run_gunicorn.sh <FRAMEWORK>


where ``FRAMEWORK`` is "bottle", "flask", "falcon" and whatever else is
implemented.

All of them are listening to ``/submit`` as an HTTP GET (for convenience).
