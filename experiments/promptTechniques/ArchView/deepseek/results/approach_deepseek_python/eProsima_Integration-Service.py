from diagrams import Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import RabbitMQ
from diagrams.aws.network import CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.general import Client

with Diagram("System Architecture", show=False, direction="TB"):
    client = Client("Client")
    
    cdn = CloudFront("CDN")
    load_balancer = Server("Load Balancer")
    
    web_server1 = Server("Web Server 1")
    web_server2 = Server("Web Server 2")
    app_server1 = Server("App Server 1")
    app_server2 = Server("App Server 2")
    
    database = PostgreSQL("Database")
    cache = Redis("Cache")
    queue = RabbitMQ("Message Queue")
    storage = S3("Object Storage")
    
    client >> cdn >> load_balancer
    load_balancer >> web_server1
    load_balancer >> web_server2
    web_server1 >> app_server1
    web_server2 >> app_server2
    app_server1 >> database
    app_server1 >> cache
    app_server1 >> queue
    app_server1 >> storage
    app_server2 >> database
    app_server2 >> cache
    app_server2 >> queue
    app_server2 >> storage
    cache >> database
    queue >> app_server1
    queue >> app_server2