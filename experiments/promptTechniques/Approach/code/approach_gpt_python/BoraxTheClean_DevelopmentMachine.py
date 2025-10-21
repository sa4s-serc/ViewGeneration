from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAMRole
from diagrams.aws.network import VPC
from diagrams.aws.general import GenericFirewall
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import User
from diagrams.onprem.vcs import Github

with Diagram("BoraxTheClean_DevelopmentMachine Architecture", show=False):
    user = User("Developer")

    with Cluster("AWS Cloud"):
        vpc = VPC("VPC")
        
        with Cluster("EC2 Deployment"):
            ec2 = EC2("Amazon Linux EC2")
            iam_role = IAMRole("IAM Instance Profile")
            sg = GenericFirewall("Security Group")
            cloudwatch_alarm = Cloudwatch("Inactivity Alarm")
        
        ec2 - sg
        ec2 << iam_role
        ec2 >> cloudwatch_alarm
        
    with Cluster("CI/CD Pipeline"):
        github_actions = GithubActions("GitHub Actions")
        github_repo = Github("Repository")
        
        github_repo >> github_actions
        github_actions >> ec2
        
    user >> github_repo