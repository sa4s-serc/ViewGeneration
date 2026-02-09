from diagrams import Diagram
from diagrams.programming.framework import Django
from diagrams.onprem.database import MySQL
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.vcs import Github
from diagrams.onprem.container import Docker

with Diagram("Linux Command Tutorial Architecture", show=False):
    git = Github("GitHub\nRepository")
    
    web = Django("Documentation\nWebsite")
    
    db = MySQL("MySQL\nMetadata")
    
    cache = Redis("Redis\nCache")
    
    queue = RabbitMQ("Message\nQueue")
    
    container = Docker("Docker\nContainer")

    git >> web
    web >> db
    web >> cache 
    web >> queue
    queue >> container