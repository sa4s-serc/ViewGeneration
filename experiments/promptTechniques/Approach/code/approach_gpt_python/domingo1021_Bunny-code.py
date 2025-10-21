from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS
from diagrams.aws.network import ELB
from diagrams.onprem.client import Users
from diagrams.programming.flowchart import Action
from diagrams.programming.language import Nodejs
from diagrams.custom import Custom

with Diagram("Bunny Code Platform Architecture", show=False, direction="LR"):
    users = Users("Users")

    with Cluster("Web Application"):
        api = Nodejs("API Server")
        socket = Nodejs("Socket.IO")

    with Cluster("Database Layer"):
        mysql = RDS("MySQL")
        influxdb = Custom("InfluxDB", "./influxdb.png")
        redis = Custom("Redis", "./redis.png")

    with Cluster("Sandbox Environment"):
        docker = Custom("Docker", "./docker.png")

    with Cluster("Cloud Services"):
        s3 = Custom("S3", "./s3.png")
        cloudfront = Custom("CloudFront", "./cloudfront.png")
        cloudwatch = Custom("CloudWatch", "./cloudwatch.png")

    users >> Edge(label="HTTP/HTTPS", style="dashed") >> api
    users >> Edge(label="WebSocket", style="dashed") >> socket

    api >> Edge(label="JDBC") >> mysql
    api >> Edge(label="HTTP") >> influxdb
    api >> Edge(label="TCP") >> redis

    api >> Edge(label="REST API") >> docker

    docker >> Edge(label="Store") >> s3
    docker >> Edge(label="CDN") >> cloudfront
    docker >> Edge(label="Logs") >> cloudwatch

    socket >> Edge(label="Real-time Updates") >> redis