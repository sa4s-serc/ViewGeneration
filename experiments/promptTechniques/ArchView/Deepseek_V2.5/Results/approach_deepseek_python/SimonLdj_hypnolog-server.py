from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.compute import Server

with Diagram("Architectural View", show=False):
    user = User("User")
    load_balancer = Nginx("Load Balancer")
    web_server = Server("Web Server")
    database = Postgresql("Database")
    cache = Redis("Cache")

    user >> load_balancer >> web_server
    web_server >> database
    web_server >> cache