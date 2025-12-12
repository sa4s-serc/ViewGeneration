from diagrams import Diagram, Cluster
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import RabbitMQ
from diagrams.programming.language import Typescript
from diagrams.onprem.container import Docker
from diagrams.programming.language import NodeJS

with Diagram("User Authentication and Management API Architecture", show=False):
    with Cluster("API Layer"):
        api = NodeJS("API Server")
        ts = Typescript("TypeScript")

    with Cluster("Data Layer"):
        db = PostgreSQL("PostgreSQL")
        cache = Redis("Redis Cache")
        queue = RabbitMQ("Message Queue")

    with Cluster("Infrastructure"):
        docker = Docker("Container")

    # Connect components showing data flow
    ts >> api
    api >> db
    api >> cache 
    api >> queue
    docker >> [api, db, cache, queue]