from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import CloudFront, ELB
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.onprem.container import Docker
from diagrams.onprem.database import MySQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import InfluxDB
from diagrams.onprem.network import Nginx

with Diagram("Bunny Code Platform Architecture", show=False, direction="TB"):
    with Cluster("Cloud Services"):
        cdn = CloudFront("CDN")
        s3 = S3("S3 Storage")
        cloudwatch = EC2("CloudWatch")

    with Cluster("Backend Services"):
        with Cluster("Load Balancer"):
            nginx = Nginx("Nginx")
        
        with Cluster("Application Layer"):
            app = EC2("Node.js/Express")
            socket = EC2("Socket.IO")
        
        with Cluster("Authentication"):
            auth = Cognito("JWT Auth")
        
        with Cluster("Database Layer"):
            mysql = MySQL("MySQL")
            influxdb = InfluxDB("InfluxDB")
            redis = Redis("Redis")
        
        with Cluster("Sandbox"):
            docker = Docker("Docker Sandbox")

    cdn >> nginx
    nginx >> app
    app >> auth
    app >> mysql
    app >> influxdb
    app >> redis
    app >> docker
    socket >> app
    app >> s3
    app >> cloudwatch