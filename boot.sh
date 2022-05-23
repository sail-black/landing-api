#!/bin/sh
exec gunicorn -b :8080 --access-logfile access.log --error-logfile error.log microblog:app
