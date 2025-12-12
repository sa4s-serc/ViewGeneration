from diagrams import Diagram, Cluster
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.logging import Fluentbit
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Envoy
from diagrams.programming.language import Java
from diagrams.programming.language import Javascript

with Diagram("HTTP Proxy Service Architecture", show=False):
    client = Server("Client")
    
    with Cluster("Proxy Service"):
        proxy_server = Nginx("HttpProxyServer")
        
        with Cluster("Request Processing"):
            client_handler = Java("ClientToProxyHandler")
            server_handler = Java("ProxyToServerHandler")
            
        with Cluster("Filters"):
            request_filters = Java("Request Filters")
            response_filters = Java("Response Filters")
            
        with Cluster("Configuration"):
            entity_manager = Java("EntitysManager")
            config_file = PostgreSQL("entitys.json")
            
        with Cluster("Exception Handling"):
            exception_handler = Java("GlobalExceptionHandler")
            msg_translator = Java("MsgTranslater")
    
    with Cluster("Backend Services"):
        test_server = Javascript("TestServer")
        test_client = Javascript("TestClient")
        backend_servers = [Server("Backend 1"), Server("Backend 2")]
    
    with Cluster("Monitoring"):
        logging = Fluentbit("Logging")
        monitoring = Grafana("Monitoring")
        metrics = Redis("Metrics Cache")
    
    client >> proxy_server
    proxy_server >> client_handler
    client_handler >> request_filters
    client_handler >> entity_manager
    entity_manager >> config_file
    client_handler >> server_handler
    server_handler >> response_filters
    server_handler >> backend_servers
    backend_servers >> server_handler
    server_handler >> client_handler
    client_handler >> proxy_server
    proxy_server >> client
    
    proxy_server >> exception_handler
    exception_handler >> msg_translator
    
    test_client >> proxy_server
    proxy_server >> test_server
    
    [proxy_server, client_handler, server_handler] >> logging
    logging >> monitoring
    logging >> metrics