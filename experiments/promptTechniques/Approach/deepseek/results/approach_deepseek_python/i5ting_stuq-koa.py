from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MongoDB
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.inmemory import Redis

with Diagram("Koa.js Web Application Architecture", show=False, direction="TB"):
    users = User("Users")
    
    with Diagram("Presentation Layer"):
        frontend = Server("Frontend App")
        admin = Server("Admin Panel")
        
    with Diagram("Application Layer"):
        api = Server("API Server")
        middleware = Server("Middleware")
        
    with Diagram("Data Layer"):
        database = MongoDB("MongoDB")
        cache = Redis("Redis Cache")
        
    with Diagram("Supporting Services"):
        ci_cd = Jenkins("CI/CD")
        monitoring = Grafana("Monitoring")
        scheduler = Airflow("Workflow Scheduler")
        container = Docker("Container Runtime")
    
    # Connections
    users >> frontend
    users >> admin
    frontend >> api
    admin >> api
    api >> middleware
    middleware >> database
    middleware >> cache
    ci_cd >> container
    container >> api
    api >> monitoring
    scheduler >> api