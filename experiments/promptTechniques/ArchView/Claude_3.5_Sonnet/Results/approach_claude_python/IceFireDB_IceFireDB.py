from diagrams import Diagram, Cluster
from diagrams.aws.database import RDS, Dynamodb, ElasticacheForRedis
from diagrams.aws.network import ELB
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS
from diagrams.aws.security import IAM
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service

with Diagram("IceFireDB Architecture", show=False):
    with Cluster("Security Layer"):
        auth = IAM("Authentication")

    with Cluster("Load Balancer"):
        lb = ELB("Load Balancer")

    with Cluster("Application Layer"):
        with Cluster("IceFireDB Core"):
            core = [Pod("IceFireDB Instance") for _ in range(3)]
        
        with Cluster("SQL Proxy"):
            proxy = Service("SQL Proxy")
            proxy_instances = [Pod("SQLProxy Instance") for _ in range(2)]

    with Cluster("Storage Layer"):
        leveldb = Dynamodb("LevelDB Storage")
        redis_cache = ElasticacheForRedis("Redis Protocol")
        mysql = RDS("MySQL Backend")
        object_store = S3("Object Storage")

    with Cluster("Message Queue"):
        queue = SQS("Event Queue")

    # Connect components
    lb >> core
    lb >> proxy
    proxy >> proxy_instances
    auth >> lb
    
    proxy_instances >> mysql
    core >> leveldb
    core >> redis_cache
    core >> object_store
    core >> queue
    proxy_instances >> queue