from diagrams import Diagram
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.database import Mongodb
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.programming.language import Python
from diagrams.generic.blank import Blank

with Diagram("OpenHub Architecture", show=False, direction="TB"):
    github = Client("GitHub")
    
    crawler = Server("Crawler")
    crawler - github
    
    rabbitmq = Rabbitmq("RabbitMQ")
    crawler >> rabbitmq
    
    worker_manager = Server("Worker Manager")
    rabbitmq >> worker_manager
    
    analysis_modules = [
        Python("Security Analysis"),
        Python("Testability Analysis"),
        Python("Reusability Analysis"),
        Python("Usability Analysis")
    ]
    
    worker_manager >> analysis_modules
    
    mongodb = Mongodb("MongoDB")
    analysis_modules >> mongodb