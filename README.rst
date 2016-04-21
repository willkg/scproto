=======
scproto
=======

This repo holds some prototyping I fiddled with for the new Socorro
collector.

It contains two scripts:

* ``run_gunicorn.sh``: Runs gunicorn with the specified framework.
* ``run_siege.sh``: The siege thing I was running.

It has rough sketches of a collector implemented with:

* `bottle <http://bottlepy.org/docs/dev/index.html>`_
* `flask <http://flask.pocoo.org/>`_
* `falcon <http://falconframework.org/>`_

It's released under the MPLv2.
