#!/bin/bash
DJANGO_SETTINGS_MODULE=settings_production venv/bin/gunicorn --bind 127.0.0.1:8001 wsgi --daemon
