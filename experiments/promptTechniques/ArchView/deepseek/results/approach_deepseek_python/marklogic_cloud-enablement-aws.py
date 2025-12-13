from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, ECS, Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import VPC, ELB, Route53, CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudformation
from diagrams.aws.security import IAM
from diagrams.aws.integration import SNS

with Diagram("MarkLogic Cloud Enablement on AWS", show=False, direction="TB"):
    dns = Route53("Route53")
    cdn = CloudFront("CloudFront")
    
    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            alb = ELB("ALB")
            
            with Cluster("Auto Scaling Group"):
                with Cluster("Availability Zone 1"):
                    ml_node1 = EC2("MarkLogic\nNode 1")
                    ml_node2 = EC2("MarkLogic\nNode 2")
                
                with Cluster("Availability Zone 2"):
                    ml_node3 = EC2("MarkLogic\nNode 3")
                    ml_node4 = EC2("MarkLogic\nNode 4")
            
            with Cluster("Lambda Functions"):
                managed_eni = Lambda("managedeni.py")
                node_manager = Lambda("nodemanager.py")
                utils = Lambda("utils.py")
        
        cloudformation = Cloudformation("CloudFormation")
        dynamodb = Dynamodb("DynamoDB\nCluster State")
        s3 = S3("S3\nTemplates")
        iam = IAM("IAM Roles")
        sns = SNS("SNS\nLogging")
    
    dns >> cdn >> alb
    alb >> [ml_node1, ml_node2, ml_node3, ml_node4]
    
    cloudformation >> [s3, iam, dynamodb, sns]
    cloudformation >> VPC("VPC") >> alb
    
    managed_eni >> ml_node1
    managed_eni >> ml_node2
    managed_eni >> ml_node3
    managed_eni >> ml_node4
    
    node_manager >> managed_eni
    node_manager >> dynamodb
    utils >> managed_eni
    utils >> node_manager
    
    ml_node1 >> dynamodb
    ml_node2 >> dynamodb
    ml_node3 >> dynamodb
    ml_node4 >> dynamodb