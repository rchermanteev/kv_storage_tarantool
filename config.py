import os


DEBUG = int(os.environ.get("DEBUG", 1))
ENABLE_AUTORELOAD = int(os.environ.get("ENABLE_AUTORELOAD", DEBUG))

CR_HOST = os.environ.get("CR_HOST", "0.0.0.0")
CR_PORT = int(os.environ.get("CR_PORT", 8001))

SENTRY_DSN = ""
