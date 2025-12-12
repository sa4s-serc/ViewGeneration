from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.management import Cloudwatch, Cloudformation
from diagrams.aws.security import IAM
from diagrams.aws.network import ELB
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions
from diagrams.aws.storage import S3

with Diagram("BoraxTheClean Development Machine Architecture", show=False, direction="TB"):
    github = Github("GitHub Repository")
    github_actions = GithubActions("GitHub Actions\nCI/CD Pipeline")
    
    cloudformation = Cloudformation("CloudFormation\nTemplate")
    
    iam_role = IAM("IAM Role\n(AdministratorAccess)")
    security_group = ELB("Security Group\n(SSH from all IPs)")
    ec2_instance = EC2("EC2 Instance\nAmazon Linux")
    
    cloudwatch_alarm = Cloudwatch("CloudWatch Alarm\nInactivity Shutdown")
    
    s3_bucket = S3("S3 Bucket\nTemplate Storage")
    
    github >> github_actions
    github_actions >> cloudformation
    cloudformation >> [iam_role, security_group, ec2_instance]
    cloudformation >> s3_bucket
    cloudwatch_alarm >> ec2_instance
    iam_role >> ec2_instance
    security_group >> ec2_instance