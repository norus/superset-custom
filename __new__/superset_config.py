import logging
import os
from cachelib.file import FileSystemCache
from celery.schedules import crontab
from cachelib.redis import RedisCache

logger = logging.getLogger()

def get_env_variable(var_name, default=None):
    '''Get the environment variable or raise exception.'''
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = 'The environment variable {} was missing, abort...'.format(
                var_name
            )
            raise EnvironmentError(error_msg)


DATABASE_DIALECT = get_env_variable('DATABASE_DIALECT')
DATABASE_USER = get_env_variable('DATABASE_USER')
DATABASE_PASSWORD = get_env_variable('DATABASE_PASSWORD')
DATABASE_HOST = get_env_variable('DATABASE_HOST')
DATABASE_PORT = get_env_variable('DATABASE_PORT')
DATABASE_DB = get_env_variable('DATABASE_DB')

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = '%s://%s:%s@%s:%s/%s' % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)

REDIS_HOST = get_env_variable('REDIS_HOST')
REDIS_PORT = get_env_variable('REDIS_PORT')
REDIS_CELERY_DB = get_env_variable('REDIS_CELERY_DB')
REDIS_RESULTS_DB = get_env_variable('REDIS_RESULTS_DB')

# From https://superset.apache.org/docs/installation/async-queries-celery
from cachelib.redis import RedisCache
RESULTS_BACKEND = RedisCache(
    host=REDIS_HOST, port=REDIS_PORT, key_prefix='superset_results')

class CeleryConfig(object):
    BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}'
    CELERY_IMPORTS = (
        'superset.sql_lab',
        'superset.tasks',
    )
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}'
    CELERY_ANNOTATIONS = {
        'sql_lab.get_sql_results': {
            'rate_limit': '100/s',
        },
        'email_reports.send': {
            'rate_limit': '1/s',
            'time_limit': 120,
            'soft_time_limit': 150,
            'ignore_result': True,
        },
    }

    CELERY_TASK_PROTOCOL = 1
    CELERYBEAT_SCHEDULE = {
        # By default, Beat will check for new tasks at 1-minute of every hour
        # E.g. at 12:01, 13:01, etc.
        'email_reports.schedule_hourly': {
            'task': 'email_reports.schedule_hourly',
            'schedule': crontab(minute='1', hour='*'),
        },
    }


CELERY_CONFIG = CeleryConfig
SQLLAB_CTAS_NO_LIMIT = True

WEBDRIVER_WINDOW = {"dashboard": (1600, 2000), "slice": (3000, 1200)}
WEBDRIVER_BASEURL = "http://superset_app:8080/"

# Email settings start here
ENABLE_SCHEDULED_EMAIL_REPORTS=True
SMTP_HOST='smtp.gmail.com'
SMTP_STARTTLS=True
SMTP_SSL=False
SMTP_USER='xxx@gmail.com'
SMTP_PORT=587
SMTP_PASSWORD='xxx'
SMTP_MAIL_FROM='xxx@gmail.com'
EMAIL_NOTIFICATIONS=True
EMAIL_REPORT_FROM_ADDRESS='xxx@gmail.com'
EMAIL_REPORT_BCC_ADDRESS=None
# This user needs to be an admin user
EMAIL_REPORTS_USER='admin'
EMAIL_REPORTS_SUBJECT_PREFIX="[Superset Report] "
EMAIL_REPORTS_WEBDRIVER='firefox'
