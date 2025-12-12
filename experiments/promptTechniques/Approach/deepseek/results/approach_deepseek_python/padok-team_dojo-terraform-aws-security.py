from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB, VPC, InternetGateway, RouteTable, PublicSubnet, PrivateSubnet
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch
from diagrams.aws.storage import S3
from diagrams.onprem.client import User

with Diagram("Terraform Security Dojo Architecture", show=False, direction="TB"):
    user = User("Developer")
    
    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            igw = InternetGateway("Internet Gateway")
            
            with Cluster("Public Subnet"):
                alb = ELB("Application Load Balancer")
                
            with Cluster("Private Subnet"):
                with Cluster("Development Environment"):
                    dev_ec2 = EC2("Dev EC2 Instance")
                    
                with Cluster("Production Environment"):
                    prd_ec2 = EC2("Prod EC2 Instance")
        
        iam = IAM("IAM Roles & Policies")
        cloudwatch = Cloudwatch("CloudWatch Monitoring")
        s3 = S3("Terraform State Storage")
    
    user >> igw
    igw >> alb
    alb >> dev_ec2
    alb >> prd_ec2
    
    iam - [dev_ec2, prd_ec2]
    cloudwatch - [dev_ec2, prd_ec2]
    s3 - [dev_ec2, prd_ec2]