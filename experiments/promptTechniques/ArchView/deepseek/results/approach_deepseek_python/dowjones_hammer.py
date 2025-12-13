from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SNS
from diagrams.aws.security import IAM
from diagrams.onprem.client import User
from diagrams.saas.chat import Slack
from diagrams.saas.alerting import Opsgenie
from diagrams.aws.network import VPC

with Diagram("Dow Jones Hammer Architecture", show=False, direction="TB"):
    user = User("User")
    slack = Slack("Slack")
    jira = Opsgenie("JIRA")
    
    with Cluster("AWS VPC"):
        with Cluster("Data Layer"):
            aws_resources = [S3("S3"), Dynamodb("DynamoDB")]
        
        with Cluster("Identification Layer"):
            initiation_lambda = Lambda("Initiation Lambda")
            identification_lambda = Lambda("Identification Lambda")
            sns = SNS("SNS")
            initiation_lambda >> sns >> identification_lambda
        
        with Cluster("Reporting Layer"):
            ec2_reporting = EC2("Reporting EC2")
            ec2_reporting >> jira
            ec2_reporting >> slack
        
        with Cluster("Remediation Layer"):
            ec2_remediation = EC2("Remediation EC2")
        
        identification_lambda >> aws_resources
        identification_lambda >> ec2_reporting
        ec2_reporting >> ec2_remediation
        ec2_remediation >> aws_resources
    
    user >> slack
    user >> jira