from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Angular
from diagrams.programming.framework import Dotnet
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.container import Docker

with Diagram("Contact Management Application Architecture", show=False, direction="TB"):

    user = User("User")

    with Cluster("Frontend"):
        angular_app = Angular("Angular App")

    with Cluster("Backend"):
        web_api = Dotnet("ASP.NET Core Web API")
        with Cluster("Application Layer"):
            application_logic = Dotnet("Logic & CQRS")
        with Cluster("Domain Layer"):
            domain_entities = Dotnet("Domain Entities")
        with Cluster("Infrastructure Layer"):
            persistence = Dotnet("Persistence")
            identity = Dotnet("Identity")

    with Cluster("Database"):
        postgres = PostgreSQL("PostgreSQL")

    with Cluster("Containerization"):
        docker = Docker("Docker")
        docker_compose = Docker("Docker Compose")

    user >> Edge(label="HTTP Request") >> angular_app
    angular_app >> Edge(label="API Call") >> web_api
    web_api >> Edge(label="Command/Query") >> application_logic
    application_logic >> Edge(label="Access Domain") >> domain_entities
    application_logic >> Edge(label="Data Access") >> persistence
    application_logic >> Edge(label="Auth") >> identity
    persistence >> Edge(label="Read/Write") >> postgres

    with Cluster("Load Balancer"):
        nginx = Nginx("NGINX")
        nginx >> Edge(label="Distribute Traffic") >> [angular_app, web_api]

    docker >> Edge(label="Containerize") >> [angular_app, web_api, postgres, nginx]
    docker_compose >> Edge(label="Orchestrate") >> docker