import os


class Config:
    APP_ID = int(os.environ.get("APP_ID"))
    API_HASH = os.environ.get("API_HASH")