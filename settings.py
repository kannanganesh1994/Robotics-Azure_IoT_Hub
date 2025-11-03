import os
from dotenv import load_dotenv
load_dotenv(override=False)

class Settings:
    IOTH_DEVICE_CONN_STRING = os.getenv("IOTH_DEVICE_CONN_STRING")