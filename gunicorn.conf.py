bind = "0.0.0.0:8000"

workers = 2
worker_class = "sync"
threads = 1

timeout = 30
graceful_timeout = 30
keepalive = 2

accesslog = "-"
errorlog = "-"
logleve = "info"

reload = True
