from diagrams import Diagram, Cluster
from diagrams.programming.framework import Spring, Django
from diagrams.programming.language import Java, Python
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import RabbitMQ

with Diagram("OpenPSD Model Bank Clean Architecture", show=False):
    with Cluster("Presentation Layer"):
        controller = Spring("ModelBank Controller")

    with Cluster("Application Layer"):
        usecase = Django("ModelBank Usecase")

    with Cluster("Domain Layer"):
        entities = Java("Domain Entities")
        processors = Python("Domain Processors")

    with Cluster("Infrastructure Layer"):
        db = PostgreSQL("Database Provider")
        queue = RabbitMQ("Message Queue")

    # Define relationships
    controller >> usecase
    usecase >> entities
    usecase >> processors
    entities >> db
    processors >> queue
    processors >> db