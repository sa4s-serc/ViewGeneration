from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.network import Gunicorn
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Celery

with Diagram("Web Application Architecture", show=False, direction="LR"):
    user = User("User")
    
    with Diagram("Application Layer"):
        web_server = Gunicorn("Web Server")
        app_servers = [Gunicorn("App Server 1"), Gunicorn("App Server 2")]
        
    with Diagram("Data Layer"):
        database = PostgreSQL("PostgreSQL")
        cache = Redis("Redis Cache")
        queue = Celery("Message Queue")
    
    user >> web_server
    web_server >> app_servers
    app_servers >> database
    app_servers >> cache
    app_servers >> queue