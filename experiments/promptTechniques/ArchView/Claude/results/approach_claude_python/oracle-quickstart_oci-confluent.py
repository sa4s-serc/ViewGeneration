from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import VPC, InternetGateway, Route53
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS
from diagrams.aws.security import IAM
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import Oracle

with Diagram("Oracle Quickstart OCI Confluent Architecture", show=False):
    
    # Network Components
    vpc = VPC("Virtual Network")
    igw = InternetGateway("Internet Gateway")

    # Security
    iam = IAM("Security & IAM")

    # Storage
    s3 = S3("Object Storage")
    
    # Compute Instances
    kafka_brokers = [EC2("Kafka Broker") for _ in range(3)]
    zk_nodes = [EC2("Zookeeper") for _ in range(3)]
    schema_registry = EC2("Schema Registry")
    rest_proxy = EC2("REST Proxy")
    connect = EC2("Kafka Connect")
    ksql = EC2("KSQL")
    control_center = EC2("Control Center")

    # Databases
    oracle_db = Oracle("Oracle ADW/ATP")
    
    # Message Queue
    kafka = Kafka("Confluent Kafka")
    message_queue = SQS("Message Queue")

    # Network Flow
    igw >> vpc
    vpc >> iam
    
    # Connect components
    vpc >> kafka_brokers
    vpc >> zk_nodes
    vpc >> schema_registry
    vpc >> rest_proxy
    vpc >> connect
    vpc >> ksql
    vpc >> control_center
    
    # Data Flow
    kafka_brokers >> kafka
    kafka >> connect
    connect >> oracle_db
    connect >> s3
    kafka >> message_queue