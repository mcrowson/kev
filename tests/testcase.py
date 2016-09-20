import unittest
from kev.loading import KevHandler
from envs import env
import placebo
from boto3 import Session
import os


def test_session():
    placebo_dir = os.path.join(os.path.dirname(__file__), 'placebo')
    session = Session()
    pill = placebo.attach(session, data_path=placebo_dir)
    if env('PLACEBO_MODE') == 'record':
        pill.record()
    else:
        pill.playback()
    return session

kev_handler = KevHandler({
    's3':{
        'backend':'kev.backends.s3.db.S3RedisDB',
        'connection':{
            'bucket':env('S3_BUCKET_TEST'),
            'indexer':{
                'host':env('REDIS_HOST_TEST'),
                'port':env('REDIS_PORT_TEST'),
            },
            'session': test_session()
        }
    },
    'redis': {
        'backend': 'kev.backends.redis.db.RedisDB',
        'connection': {
            'host': env('REDIS_HOST_TEST'),
            'port': env('REDIS_PORT_TEST'),
        }
    }
})

class KevTestCase(unittest.TestCase):

    def tearDown(self):
        for db_label in list(kev_handler._databases.keys()):
            kev_handler.get_db(db_label).flush_db()