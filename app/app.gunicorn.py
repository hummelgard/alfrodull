chdir = "/srv/http/app/"
#worker_class = "sync" 
worker_class = "gevent"
#worker_connections ="1"
errorlog = "/srv/http/app/log/app.gunicorn.log" 
pid = "/srv/http/app/run/pid"

