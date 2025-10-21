from diagrams import Diagram, Cluster, Edge
from diagrams.aws.security import IAM, WAF, Shield
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.database import Dynamodb, RDS
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import APIGateway
from diagrams.onprem.client import Users
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.iac import Terraform
from diagrams.onprem.vcs import Github

with Diagram("Dow Jones Hammer Architecture", show=False, direction="TB"):

    with Cluster("AWS Environment"):
        with Cluster("Data Layer"):
            s3 = S3("S3")
            rds = RDS("RDS")
            dynamodb = Dynamodb("DynamoDB")

        with Cluster("Identification Layer"):
            lambda_initiation = Lambda("Initiation Lambda")
            lambda_identification = Lambda("Identification Lambda")
            sns = SNS("SNS")

        with Cluster("Reporting Layer"):
            ec2 = EC2("EC2")
            cloudwatch = Cloudwatch("CloudWatch")

        with Cluster("Remediation Layer"):
            lambda_remediation = Lambda("Remediation Lambda")

    with Cluster("External Services"):
        jira = Users("JIRA")
        slack = Users("Slack Bot")
        github = Github("GitHub")
        terraform = Terraform("Terraform")
        grafana = Grafana("Grafana")

    with Cluster("DevOps Tools"):
        api_gateway = APIGateway("API Gateway")

    sns >> Edge(label="triggers") >> lambda_identification
    lambda_initiation >> Edge(label="initiates") >> sns
    lambda_identification >> Edge(label="logs to") >> cloudwatch
    lambda_identification >> Edge(label="stores issues") >> dynamodb
    ec2 >> Edge(label="fetches data") >> rds
    ec2 >> Edge(label="fetches logs") >> cloudwatch
    ec2 >> Edge(label="uploads reports") >> s3
    ec2 >> Edge(label="creates tickets") >> jira
    ec2 >> Edge(label="sends notifications") >> slack
    lambda_remediation >> Edge(label="backs up config") >> s3
    lambda_remediation >> Edge(label="modifies resources") >> rds
    terraform >> Edge(label="provisions infra") >> [rds, ec2, lambda_initiation, lambda_identification, lambda_remediation]
    github >> Edge(label="source code") >> api_gateway
    api_gateway >> Edge(label="builds & deploys") >> [ec2, lambda_initiation, lambda_identification, lambda_remediation]
    api_gateway >> Edge(label="triggers on-demand scans") >> lambda_initiation
    api_gateway >> Edge(label="retrieves results") >> ec2