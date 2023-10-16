celery -A cotacoes worker --loglevel=info -P gevent --concurrency 1 -E

celery -A cotacoes beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler