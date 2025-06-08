import os
from dotenv import load_dotenv  # llamando para leer env
load_dotenv() # llamada dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_ENGINE = os.getenv("DATABASE_ENGINE", "sqlserver") # Verifica que esta variable de entorno esté configurada correctamente
print("DATABASE_ENGINE:", DATABASE_ENGINE)

if DATABASE_ENGINE == "sqlite":
    # Configuración para SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, os.getenv('SQLITE_NAME', 'db.sqlite3')),
        }
    }
elif DATABASE_ENGINE == "postgresql":
    # Configuración para PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('POSTGRESQL_NAME'),
            'USER': os.getenv('POSTGRESQL_USER'),
            'PASSWORD': os.getenv('POSTGRESQL_PASSWORD'),
            'HOST': os.getenv('POSTGRESQL_HOST'),
            'PORT': os.getenv('POSTGRESQL_PORT'),
        }
    }
elif DATABASE_ENGINE == "mysql":
    # Configuración para MySQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_NAME'),
            'USER': os.getenv('MYSQL_USER'),
            'PASSWORD': os.getenv('MYSQL_PASSWORD'),
            'HOST': os.getenv('MYSQL_HOST'),
            'PORT': os.getenv('MYSQL_PORT'),
            'OPTIONS': {
                'sql_mode': 'traditional',
            }
        }
    }
elif DATABASE_ENGINE == "sqlserver":
    # Configuración para SQL Server
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': os.getenv('SQLSERVER_NAME'),
            'USER': os.getenv('SQLSERVER_USER'),
            'PASSWORD': os.getenv('SQLSERVER_PASSWORD'),
            'HOST': os.getenv('SQLSERVER_HOST'),
            'PORT': os.getenv('SQLSERVER_PORT'),
            'OPTIONS': {
                'driver': os.getenv('SQLSERVER_DRIVER'),
            }
        }
    }
else:
    raise ValueError("Unsupported database engine specified: {}".format(DATABASE_ENGINE))