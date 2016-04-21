workers = 1
worker_connections = 4
worker_class = 'scproto.geventlib.PoolGeventPyWSGIWorker'
# loglevel = 'debug'


def on_starting(server):
    try:
        from gunicorn.workers.ggevent import GeventWorker
    except ImportError:
        GeventWorker = None

    if GeventWorker is None or not issubclass(server.worker_class, GeventWorker):
        print 'You need to run this with our specialized worker.'
        print 'scproto.geventlib.PoolGeventPyWSGIWorker'
        assert False
