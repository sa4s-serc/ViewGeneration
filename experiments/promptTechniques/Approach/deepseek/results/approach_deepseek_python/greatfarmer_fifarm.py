from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.database import MongoDB
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Spring
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.logging import Graylog
from diagrams.generic.database import SQL

with Diagram("FIFArm Application Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Web Layer"):
        nginx = Nginx("Nginx")
        with Cluster("Spring Boot Application"):
            controllers = Spring("Controllers")
            services = Spring("Services")
            utils = Spring("Utilities")
            controllers >> services
            services >> utils
    
    with Cluster("Data Layer"):
        mongodb = MongoDB("MongoDB")
        redis = Redis("Redis Cache")
    
    with Cluster("External Services"):
        ea_api = Server("EA Sports FUT API")
        logging = Graylog("Logback")
    
    user >> nginx >> controllers
    services >> mongodb
    services >> redis
    services >> ea_api
    services >> logging