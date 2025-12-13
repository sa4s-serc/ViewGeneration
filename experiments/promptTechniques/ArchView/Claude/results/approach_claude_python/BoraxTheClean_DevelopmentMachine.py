from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.management import Cloudformation
from diagrams.aws.security import IAM
from diagrams.aws.management import CloudwatchAlarm
from diagrams.aws.network import VPC, InternetGateway
from diagrams.aws.general import Users

with Diagram("BoraxTheClean Development Machine Architecture", show=False):
    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            igw = InternetGateway("Internet Gateway")
            
            with Cluster("Public Subnet"):
                ec2 = EC2("Development EC2")
                
        iam = IAM("IAM Role\n(Administrator)")
        cfn = Cloudformation("CloudFormation Stack")
        alarm = CloudwatchAlarm("Inactivity Alarm")
        
        users = Users("Developers")
        
        # Draw relationships
        users >> igw >> ec2
        cfn >> [ec2, iam]
        iam >> ec2
        alarm >> ec2