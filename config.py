import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'campusdash-secret-key-ads-2026')
    DATABASE = os.path.join(BASE_DIR, 'instance', 'campusdash.db')
    SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')
    DEBUG = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
