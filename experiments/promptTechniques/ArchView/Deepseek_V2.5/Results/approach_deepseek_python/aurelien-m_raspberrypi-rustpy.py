from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.programming.language import Python, Rust
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.inmemory import Memcached
from diagrams.onprem.queue import Celery
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki

with Diagram("Raspberry Pi Hardware Control System Architecture", show=False, direction="TB"):
    user = User("Web User")
    
    web_server = Nginx("Web Server")
    rust_backend = Rust("Rust Backend")
    python_controller = Python("Python Controller")
    hardware_layer = Server("Hardware Layer")
    
    # Supporting services
    redis = Redis("Redis Cache")
    memcached = Memcached("Memcached")
    celery_worker = Celery("Celery Worker")
    monitoring = Grafana("Monitoring")
    logging = Loki("Logging")
    
    # Main data flow
    user >> web_server >> rust_backend
    rust_backend >> python_controller >> hardware_layer
    rust_backend >> redis
    rust_backend >> memcached
    rust_backend >> celery_worker
    rust_backend >> monitoring
    rust_backend >> logging
    
    # Feedback loop
    hardware_layer >> python_controller >> rust_backend >> web_server >> user