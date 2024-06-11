from firebase_admin import firestore, storage
from app.config import config


db: firestore.Client = None
bucket = None


def get_db():
    global db
    if db is None:
        db = firestore.client()
    return db


def get_bucket():
    global bucket
    if bucket is None:
        bucket = storage.bucket(name=config.firebase_storage_bucket)
    return bucket
