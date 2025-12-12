from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda 
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import Cognito
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Master

with Diagram("Benchmark AI Architecture", show=False, direction="TB"):
    
    with Cluster("Frontend"):
        api = APIGateway("API Gateway")
        auth = Cognito("Auth")
        
    with Cluster("Core Services"):
        bff = Lambda("BAI-BFF\n(Clojure)")
        
        with Cluster("Kubernetes Cluster"):
            k8s = Master("K8s Control")
            executor = Pod("Executor")
            watcher = Pod("Watcher") 
            fetcher = Pod("Fetcher")
            metrics = Pod("Metrics")

    with Cluster("Storage & Messaging"):
        queue = SQS("Job Queue")
        events = SNS("Event Bus") 
        storage = S3("Data Storage")
        db = Dynamodb("State DB")
        monitor = Cloudwatch("Monitoring")

    # Frontend flows
    api >> Edge(label="submit job") >> bff
    api >> Edge(label="auth") >> auth

    # Core service flows  
    bff >> Edge(label="publish") >> queue
    queue >> executor
    executor >> Edge(label="status") >> events 
    events >> watcher
    watcher >> Edge(label="update") >> db

    # Data flows
    executor >> Edge(label="fetch") >> fetcher
    fetcher >> storage
    metrics >> Edge(label="export") >> monitor

    # Infrastructure
    k8s >> Edge() >> [executor, watcher, fetcher, metrics]

    # State management
    bff >> Edge(label="query") >> db
    watcher >> Edge(label="metrics") >> monitor