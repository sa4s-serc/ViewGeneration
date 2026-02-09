from diagrams import Diagram, Cluster
from diagrams.aws.network import APIGateway
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.compute import ContainerInstances
from diagrams.azure.database import CosmosDb
from diagrams.gcp.analytics import PubSub
from diagrams.azure.storage import StorageAccounts

with Diagram("Airline Microservices Architecture", show=False):
    with Cluster("API Layer"):
        gateway = APIGateway("API Gateway")

    with Cluster("Authentication"):
        auth = ActiveDirectory("Identity Service")

    with Cluster("Core Services"):
        flight = ContainerInstances("Flight Service")
        passenger = ContainerInstances("Passenger Service")
        reservation = ContainerInstances("Reservation Service")

    with Cluster("Data Layer"):
        db = CosmosDb("Database")
        storage = StorageAccounts("Storage")

    with Cluster("Messaging"):
        queue = PubSub("Message Broker")

    # Connect components
    gateway >> [flight, passenger, reservation]
    gateway >> auth
    auth >> [flight, passenger, reservation]
    flight >> db
    passenger >> db
    reservation >> db
    flight >> queue
    passenger >> queue
    reservation >> queue
    [flight, passenger, reservation] >> storage