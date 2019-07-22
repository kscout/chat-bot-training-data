#!/bin/sh

# Prepare log files and start outputting logs to stdout
mkdir -p logs
touch logs/gunicorn.log
# touch logs/gunicorn-access.log
tail -n 0 -f logs/gunicorn*.log &

export NLTK_DATA=/srv/bot_api/nltk_data/

exec gunicorn app:app \
    --bind 0.0.0.0:8080 \
    --workers 5 \
    --log-level=info \
    --log-file=logs/gunicorn.log \
"$@"