web: gunicorn wsgi -w 8 -b :$PORT --access-logfile - --error-logfile - --access-logformat '[%(h)s] %({request_id}i)s %(u)s %(t)s "%(r)s" %(s)s %(D)s %(b)s "%(f)s" "%(a)s"'
pworker: python manage.py celery worker -Q pipeline -n pipeline_worker@%h -c 6 -l info --maxtasksperchild=50
sworker: celery worker -A blueapps.core.celery -P gevent -Q service_schedule -c 6 -l info -n schedule_worker@%h --maxtasksperchild=50
cworker: python manage.py celery worker -Q pipeline_additional_task -n common_worker@%h -c 6 -l info --maxtasksperchild=50
beat: python manage.py celery beat -l info
# redis: /app/redis-server /app/redis.conf # 暂时使用 paas v2 的 redis 资源
python manage.py celery worker -l info
python manage.py celery beat -l info
