from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent


LOCAL_SQLITE_DB = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

LOCAL_POSTGRES_DB = {

    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get('LOCAL_POSTGRES_DB_NAME'),
    'USER': os.environ.get('POSTGRES_DB_USER'),
    'PASSWORD': os.environ.get('LOCAL_POSTGRES_DB_PASSWORD'),
    'HOST': os.environ.get('LOCAL_POSTGRES_DB_HOST'),
    'PORT': os.environ.get('LOCAL_POSTGRES_DB_PORT'),

}

AWS_POSTGRES_DB = {

        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('AWS_POSTGRES_DB_NAME'),
        'USER': os.environ.get('POSTGRES_DB_USER'),
        'PASSWORD': os.environ.get('AWS_POSTGRES_DB_PASSWORD'),
        'HOST': os.environ.get('AWS_POSTGRES_DB_HOST'),
        'PORT': os.environ.get('AWS_POSTGRES_DB_PORT'),
}