from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.integration import SQS
from diagrams.aws.security import IAM

with Diagram("AI Model Deployment Architecture", show=False, direction="LR"):
    with Cluster("Security Layer"):
        iam = IAM("Access Control")

    with Cluster("Model Processing"):
        model = SagemakerModel("AI Models")
        storage = S3("Model Storage")
        queue = SQS("Processing Queue")

    with Cluster("Deployment Infrastructure"):
        lb = ELB("Load Balancer")
        with Cluster("Processing Servers"):
            servers = [EC2("Server 1"),
                      EC2("Server 2")]
        db = RDS("Model Metadata")

    iam >> model
    model >> storage
    storage >> queue
    queue >> lb
    lb >> servers
    servers >> db