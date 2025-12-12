from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.integration import SNS
from diagrams.aws.management import Cloudwatch, Cloudformation
from diagrams.aws.security import IAM, SecretsManager
from diagrams.aws.database import RDS
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions
from diagrams.programming.language import NodeJS
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront
from diagrams.aws.analytics import Kinesis
from diagrams.aws.general import InternetAlt1

with Diagram("Enterprise CMCS Appian Connector Architecture", show=False, direction="TB"):
    github = Github("Git Repository")
    
    with Cluster("CI/CD Pipeline"):
        github_actions = GithubActions("GitHub Actions")
        pre_commit = NodeJS("Pre-commit Hooks")
        unit_tests = NodeJS("Unit Tests")
        cfn_nag = Cloudformation("CFN Nag")
        detect_secrets = SecretsManager("Detect Secrets")
        
        github >> github_actions
        github_actions >> pre_commit
        github_actions >> unit_tests
        github_actions >> cfn_nag
        github_actions >> detect_secrets
    
    with Cluster("AWS Infrastructure"):
        with Cluster("Serverless Services"):
            with Cluster("Connector Service"):
                ecs = ECS("ECS Container")
                lambda_func = Lambda("Lambda Functions")
                ecs >> lambda_func
            
            with Cluster("Alerting Service"):
                sns = SNS("SNS Topic")
            
            with Cluster("Dashboard Service"):
                cloudwatch = Cloudwatch("CloudWatch Dashboard")
                s3_bucket = S3("S3 Storage")
                cloudfront = CloudFront("CloudFront CDN")
                s3_bucket >> cloudfront
        
        with Cluster("Configuration & Security"):
            ssm = SecretsManager("SSM Parameter Store")
            secrets_mgr = SecretsManager("Secrets Manager")
            iam = IAM("IAM Roles")
            
            ecs >> ssm
            ecs >> secrets_mgr
            ecs >> iam
            lambda_func >> ssm
            lambda_func >> secrets_mgr
            lambda_func >> iam
        
        with Cluster("Data Sources"):
            appian = InternetAlt1("Appian Source")
            bigmac = InternetAlt1("BigMAC Target")
            kafka = Kinesis("Kafka Stream")
            
            appian >> kafka
            kafka >> ecs
            ecs >> bigmac
    
    github_actions >> ecs
    github_actions >> lambda_func
    github_actions >> sns
    github_actions >> cloudwatch
    
    sns >> cloudwatch
    cloudwatch >> s3_bucket