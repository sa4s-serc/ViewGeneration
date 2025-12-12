from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import DynamodbTable
from diagrams.aws.network import ALB
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudformation 
from diagrams.aws.security import IAM
from diagrams.aws.compute import Lambda

with Diagram("MarkLogic Cloud AWS Architecture", show=False):
    with Cluster("AWS Cloud"):
        with Cluster("CloudFormation Stack"):
            cfn = Cloudformation("CloudFormation")
            
            with Cluster("Network Layer"):
                alb = ALB("Application Load Balancer")
            
            with Cluster("Compute Layer"):
                ec2_instances = [EC2("MarkLogic Node") for _ in range(3)]
            
            with Cluster("Custom Resources"):
                lambda_eni = Lambda("ENI Manager")
                lambda_node = Lambda("Node Manager")
            
            with Cluster("Storage & State"):
                dynamo = DynamodbTable("MarkLogicDDBTable")
                s3 = S3("EBS Volumes")
            
            iam = IAM("IAM Roles")

        # Connect components
        cfn >> iam
        cfn >> lambda_eni
        cfn >> lambda_node
        
        alb >> ec2_instances
        
        lambda_eni >> ec2_instances
        lambda_node >> ec2_instances
        
        for instance in ec2_instances:
            instance >> dynamo
            instance >> s3