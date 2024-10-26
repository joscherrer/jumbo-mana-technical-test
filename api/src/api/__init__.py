import os, logging
from api.api import app  # pyright: ignore[reportUnusedImport]

if os.getenv("DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
