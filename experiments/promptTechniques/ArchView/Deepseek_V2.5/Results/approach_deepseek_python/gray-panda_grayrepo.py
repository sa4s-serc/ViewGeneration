from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.network import ELB, VPC, InternetGateway
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch

with Diagram("Flare-On CTF Architecture Overview", show=False, direction="TB"):
    internet = InternetGateway("Internet")

    with Cluster("VPC Network"):
        with Cluster("Public Subnet"):
            lb = ELB("Load Balancer")
            web_server = EC2("Web Server")

        with Cluster("Private Subnet"):
            with Cluster("Application Tier"):
                app_server = EC2("Application Server")
                vm = EC2("Custom VM")
                lambda_func = Lambda("Decryption Function")

            with Cluster("Data Tier"):
                db = RDS("Database")
                storage = S3("File Storage")

    with Cluster("Security & Monitoring"):
        iam = IAM("IAM")
        monitoring = Cloudwatch("CloudWatch")

    internet >> lb >> web_server
    web_server >> app_server
    app_server >> vm
    app_server >> lambda_func
    app_server >> db
    app_server >> storage
    iam >> [web_server, app_server, vm, lambda_func, db, storage]
    monitoring >> [web_server, app_server, vm, lambda_func, db, storage]