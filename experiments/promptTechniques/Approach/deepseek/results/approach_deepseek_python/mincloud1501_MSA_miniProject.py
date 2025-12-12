from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, EKS, Lambda
from diagrams.aws.network import ELB, Route53, CloudFront
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Github

with Diagram("Microservices Architecture", show=False, direction="LR"):
    dns = Route53("Route53")
    cdn = CloudFront("CloudFront")
    
    with Cluster("Load Balancers"):
        lb = ELB("Application\nLoad Balancer")
    
    with Cluster("Kubernetes Cluster"):
        with Cluster("Ingress"):
            ingress = EKS("Ingress\nController")
        
        with Cluster("Microservices"):
            svc_a = EC2("Service A")
            svc_b = EC2("Service B")
            svc_c = EC2("Service C")
        
        with Cluster("Data Layer"):
            db = RDS("PostgreSQL")
            cache = Dynamodb("DynamoDB")
            storage = S3("Object Storage")
    
    with Cluster("Event Processing"):
        queue = SQS("Message Queue")
        events = SNS("Event Bus")
        processor = Lambda("Event\nProcessor")
    
    with Cluster("Monitoring"):
        monitoring = Cloudwatch("CloudWatch")
        iam = IAM("IAM Roles")
    
    with Cluster("CI/CD Pipeline"):
        vcs = Github("GitHub")
        ci = Jenkins("Jenkins")
        iac = Terraform("Terraform")
        registry = Docker("Container\nRegistry")
    
    dns >> cdn >> lb
    lb >> ingress
    ingress >> svc_a
    ingress >> svc_b
    ingress >> svc_c
    
    svc_a >> db
    svc_b >> cache
    svc_c >> storage
    
    svc_a >> queue
    svc_b >> events
    events >> processor
    processor >> storage
    
    svc_a >> monitoring
    svc_b >> monitoring
    svc_c >> monitoring
    
    vcs >> ci
    ci >> iac
    ci >> registry
    registry >> ingress