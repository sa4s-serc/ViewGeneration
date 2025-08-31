from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS

# Architectural metadata
view_details = {
    "summary": "A scalable web application architecture using AWS components.",
    "Concern": "scalability",
    "Behavior": "request-response and asynchronous messaging",
    "Granularity": "system",
    "Components Nature": "services and APIs",
    "Connectors Nature": "HTTP requests and message queues",
    "QAs": "scalability, fault tolerance",
    "Architecture Scope": "entire system",
    "Architectural Notation": "icons and arrows",
    "Architectural Styles": "microservices",
    "Shapes": "rectangles",
    "Colored?": "yes",
    "Connectors Direction": "mixed",
    "Legend?": "yes",
    "Nested Components?": "no",
    "Explicit Ports/Interfaces?": "no",
    "Explicit Connectors?": "no"
}

with Diagram("Scalable Web Application Architecture", show=True):
    load_balancer = ELB("Load Balancer")
    
    with Cluster("Application Cluster"):
        app_servers = [EC2("App Server 1"),
                       EC2("App Server 2"),
                       EC2("App Server 3")]

    database = RDS("Database")

    message_queue = SQS("Message Queue")
    
    load_balancer >> Edge(label="HTTP Requests") >> app_servers
    app_servers >> Edge(label="Database Queries") >> database
    app_servers >> Edge(label="Async Messages") >> message_queue
    message_queue >> Edge(label="Process Messages") >> app_servers