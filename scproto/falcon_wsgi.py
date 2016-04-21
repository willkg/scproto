import logging
import os

import falcon
import gevent

from scproto.collectorlib import (
    THROTTLE_ACCEPT,
    THROTTLE_DEFER,
    THROTTLE_REJECT,
    THROTTLE_IGNORE,
    delete_crash_from_disk,
    generate_uuid,
    notify_rabbitmq,
    save_crash_to_disk,
    store_on_s3,
    throttle,
)
from scproto.geventlib import constrained_spawn


logger = logging.getLogger('gunicorn.error')


def breakpad_handle(uuid, data, throttle_ret):
    logger.info('    begin breakpad_handle ' + uuid)

    # Save the crash to disk for temporary storage while we do stuff.
    save_crash_to_disk(uuid, data)

    # Push the crash to s3.
    store_on_s3(uuid, data)

    if throttle_ret == THROTTLE_ACCEPT:
        # Stick notifying rabbitmq in an unconstrained eventlet so it can get
        # run later. This way we can delete the crash from disk sooner.
        gevent.spawn(notify_rabbitmq, uuid)

    delete_crash_from_disk(uuid)

    logger.info('    end breakpad_handle ' + uuid)


class BreakpadSubmitter(object):
    def on_get(self, req, resp):
        # We're (ab)using uuids as both the return value for the crash id as well
        # as a way to differentiate between incoming requests for logging.
        uuid = generate_uuid()
        logger.info('BEGIN ' + uuid)

        # FIXME: I'm not sure this is right. Seems like HTML form POST data is
        # consumed from .stream and then parsed and then stuck in the same
        # place with the query string params. So either the data is there or we
        # have to consume it by hand, I think.
        data = req.query_string
        throttle_ret = throttle(data)

        if throttle_ret == THROTTLE_REJECT:
            return 'Go away'

        if throttle_ret == THROTTLE_IGNORE:
            return ''

        # Create a new eventlet for handling the breakpad crash, but create it in
        # the constrained pool.
        constrained_spawn(breakpad_handle, uuid, data, throttle_ret)

        # Alternatively, we could handle the breakpad crash in this eventlet tying
        # this eventlet in the pool up and preventing it from returning the crash
        # id to the HTTP client and then handling other incoming HTTP connections.
        # breakpad_handle(uuid, data, throttle_ret)

        logger.info('END ' + uuid)
        resp.status = falcon.HTTP_200
        resp.data = 'CrashID=%s\n' % uuid


app = falcon.API()
submitter = BreakpadSubmitter()
app.add_route('/submit', submitter)
