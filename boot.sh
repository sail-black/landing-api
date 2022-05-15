#!/bin/sh
flask db upgrade
exec gunicorn -b :8080 --access-logfile - --error-logfile - microblog:app
