from diagrams import Diagram
from diagrams.onprem.client import Client
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.queue import Celery
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.monitoring import Prometheus

with Diagram("SMEV3 Adapter Service Architecture", show=False):
    client = Client("Client")
    
    api_gateway = Nginx("Sanic API Gateway")
    query_processor = Celery("Query Processor")
    database = MongoDB("MongoDB")
    redis_cache = Redis("Redis Cache")
    smev3_adapter = Server("SMEV3 Adapter")
    xsd_loader = Server("XSD Schema Loader")
    monitoring = Prometheus("Prometheus")
    logging = Grafana("Grafana")

    client >> api_gateway >> query_processor
    query_processor >> database
    query_processor >> redis_cache
    query_processor >> smev3_adapter
    query_processor >> xsd_loader
    query_processor >> monitoring
    query_processor >> logging