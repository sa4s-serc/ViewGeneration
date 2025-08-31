from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import APIGateway
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS
from diagrams.aws.general import Users

with Diagram("System Architecture", show=False, direction="TB"):

    user = Users("Users")

    with Cluster("API Layer"):
        api_gateway = APIGateway("API Gateway")

    with Cluster("Service Layer"):
        service = ECS("Service")

    with Cluster("Data Layer"):
        database = RDS("Database")

    queue = SQS("Message Queue")

    user >> Edge(label="HTTP Request") >> api_gateway >> Edge(label="Invoke") >> service
    service >> Edge(label="Database Query") >> database
    service >> Edge(label="Send Message") >> queue
    queue >> Edge(label="Receive Message") >> service