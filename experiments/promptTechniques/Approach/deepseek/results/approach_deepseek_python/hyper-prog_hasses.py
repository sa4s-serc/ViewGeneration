from diagrams import Diagram
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Memcached
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git
from diagrams.onprem.iac import Ansible
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.database import Postgresql

with Diagram("Hasses SSE Server Architecture", show=False, direction="TB"):
    web_server = Nginx("Web Server")
    
    sse_server = Server("Hasses SSE Server")
    
    client_management = Server("Client Management")
    sse_handler = Server("SSE Handler")
    async_io = Server("Async I/O (epoll)")
    message_router = Server("Message Router")
    
    communication_channel = Rabbitmq("Communication Channel")
    
    config_file = Postgresql("Configuration")
    ssl_module = Server("SSL Support")
    logging_module = Loki("Logging")
    
    clients = [
        Server("Client 1"),
        Server("Client 2"),
        Server("Client 3")
    ]
    
    web_server >> communication_channel
    communication_channel >> sse_server
    
    sse_server >> client_management
    sse_server >> sse_handler
    sse_server >> async_io
    sse_server >> message_router
    
    config_file >> sse_server
    ssl_module >> sse_server
    logging_module >> sse_server
    
    sse_server >> clients
    message_router >> clients