from .app import get_app
from .config import get_settings
from .helpers.logger import init_logging

settings = get_settings()

init_logging()

app = get_app(settings)
