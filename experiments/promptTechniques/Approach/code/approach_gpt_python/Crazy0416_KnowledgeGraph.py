from diagrams import Diagram
from diagrams.aws.network import ALB
from diagrams.aws.compute import EC2
from diagrams.aws.database import Database
from diagrams.aws.analytics import EMR
from diagrams.aws.ml import Sagemaker
from diagrams.onprem.queue import RabbitMQ
from diagrams.programming.framework import Django

with Diagram("Architectural View", show=False):
    user = EC2("User")
    load_balancer = ALB("Load Balancer")
    web_server = Django("Web Server")
    queue = RabbitMQ("Message Queue")
    database = Database("Database")
    analytics = EMR("Analytics")
    machine_learning = Sagemaker("Machine Learning Model")

    user >> load_balancer >> web_server
    web_server >> queue
    queue >> database
    web_server >> analytics
    analytics >> machine_learning