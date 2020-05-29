#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import logging.handlers
import os
import sys

from django.conf import settings


logger = logging.getLogger(__name__)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fridgify_backend.settings.local')
    os.environ.setdefault('FB_API_KEY', "None")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if not os.path.exists('logs'):
        os.mkdir('logs')
    handler = logging.handlers.RotatingFileHandler(
        "./logs/fridgify_backend.log",
        maxBytes=10*1024*1024,
        backupCount=5,
        mode='a'
    )
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(
        format='%(asctime)s %(name)s:%(levelname)s - %(message)s',
        level=level,
        handlers=[handler]
    )

    logger.info("Application started...")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
