import logging
import uuid

import gevent

(
    THROTTLE_ACCEPT,  # save and process
    THROTTLE_DEFER,   # save, but don't process
    THROTTLE_REJECT,  # tell the client to go away
    THROTTLE_IGNORE   # ignore
) = range(4)


logger = logging.getLogger('gunicorn.error')


def s3_transfer_time():
    while True:
        for i in range(5):
            yield i * 2


SLEEP_TIME = s3_transfer_time()


def generate_uuid():
    return str(uuid.uuid4())


def throttle(req):
    return THROTTLE_ACCEPT


def save_crash_to_disk(uuid, data):
    pass


def store_on_s3(uuid, data):
    sleep_time = SLEEP_TIME.next()
    logger.info('    starting store %2d %s' % (sleep_time, uuid))
    if sleep_time:
        gevent.sleep(sleep_time)
    logger.info('    ending store   %2d %s' % (sleep_time, uuid))


def notify_rabbitmq(uuid):
    pass


def delete_crash_from_disk(uuid):
    pass
