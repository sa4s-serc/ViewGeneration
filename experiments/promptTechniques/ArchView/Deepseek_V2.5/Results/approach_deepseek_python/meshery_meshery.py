from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git

with Diagram("Meshery Architecture View", show=False, direction="TB"):
    users = User("Users")
    
    with Cluster("Meshery UI"):
        ui = Server("React/Next.js UI")
    
    with Cluster("Meshery Server"):
        server = Server("Core Server")
        graphql = Server("GraphQL API")
    
    with Cluster("Adapters Layer"):
        adapters = [
            Server("Istio Adapter"),
            Server("Linkerd Adapter"),
            Server("Consul Adapter"),
            Server("Kuma Adapter")
        ]
    
    with Cluster("Data Management"):
        database = PostgreSQL("Database")
        cache = Redis("Cache")
    
    with Cluster("Event System"):
        broker = Kafka("NATS Broker")
        meshsync = Server("MeshSync")
    
    with Cluster("Operator"):
        operator = Server("Meshery Operator")
    
    with Cluster("Monitoring & Operations"):
        monitoring = Prometheus("Monitoring")
        logging = Loki("Logging")
        dashboard = Grafana("Dashboard")
    
    with Cluster("CLI"):
        cli = Server("mesheryctl")
    
    # Connections
    users >> ui
    ui >> graphql
    server >> graphql
    graphql >> adapters
    server >> database
    server >> cache
    server >> broker
    broker >> meshsync
    operator >> meshsync
    meshsync >> database
    
    # Monitoring connections
    server >> monitoring
    adapters >> monitoring
    meshsync >> monitoring
    operator >> monitoring
    
    server >> logging
    adapters >> logging
    meshsync >> logging
    
    monitoring >> dashboard
    logging >> dashboard
    
    cli >> server