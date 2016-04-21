import gevent

from gunicorn.workers.ggevent import (
    GeventPyWSGIWorker,
    PyWSGIServer,
)


# This is a thread local, but it's actually coroutine local.
_CONSTRAINED_POOL = None


class PoolGeventPyWSGIWorker(GeventPyWSGIWorker):
    wrapped_server_class = GeventPyWSGIWorker.server_class

    def server_class(self, s, application, spawn, log, handler_class, environ, **ssl_args):
        # Note that "spawn" here is actually a gevent Pool
        global _CONSTRAINED_POOL
        _CONSTRAINED_POOL = spawn
        return self.wrapped_server_class(s, application=application, spawn=spawn, log=log, handler_class=handler_class, environ=environ, **ssl_args)


def constrained_spawn(fun, *args, **kwargs):
    """Spawn an eventlet in the constrained pool

    The constrained pool contains two things:

    1. eventlets handling incoming HTTP connections
    2. eventlets handling storing crashes on s3

    We pool these two kinds of things thus tying them together so that when the
    process has a big backlog of s3 work to do, it stops accepting HTTP
    connections and that should bubble up and eventually trigger autoscaling.

    """
    # We crate a new eventlet to create an eventlet in the constrained pool
    # otherwise creating an eventlet in the pool from the pool blocks.
    #
    # FIXME: Why does it block?
    gevent.spawn(_CONSTRAINED_POOL.spawn, fun, *args, **kwargs)
