from diagrams import Diagram, Cluster
from diagrams.generic.database import SQL
from diagrams.onprem.client import Client
from diagrams.onprem.container import Docker
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import React
from diagrams.programming.language import NodeJS

with Diagram("User Authentication and Management API", show=False, direction="TB"):
    client = Client("User")

    with Cluster("API Layer"):
        nginx = Nginx("Rate Limiting\nMiddleware")
        express = NodeJS("Express")

    with Cluster("Business Logic Layer"):
        services = [
            NodeJS("CreateUserService"),
            NodeJS("AuthenticateUserService"),
            NodeJS("ListAllUsersService"),
        ]

    with Cluster("Data Access Layer"):
        with Cluster("Repository Pattern"):
            typeorm = SQL("TypeORM\n(Postgres)")

    with Cluster("Cache Layer"):
        redis = Redis("Redis")

    with Cluster("Dependency Injection"):
        tsyringe = Docker("Tsyringe")

    client >> nginx >> express >> services
    services >> typeorm
    services >> redis
    services >> tsyringe