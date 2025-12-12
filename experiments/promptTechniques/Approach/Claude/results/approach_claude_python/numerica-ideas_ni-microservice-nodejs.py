from diagrams import Diagram, Cluster
from diagrams.programming.language import Nodejs
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis 
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SNS
from diagrams.aws.management import Cloudformation
from diagrams.onprem.vcs import Gitlab
from diagrams.aws.security import IAMRole

with Diagram("Article Management Service Architecture", show=False):
    with Cluster("Authentication"):
        auth = IAMRole("JWT Auth")
    
    with Cluster("Server Deployment"):
        app = Nodejs("Express App")
        db = MongoDB("MongoDB")
        cache = Redis("Redis Cache")
        
        app >> db
        app >> cache
        auth >> app

    with Cluster("Lambda Deployment"):
        lambda_fn = Lambda("Lambda Function") 
        sns = SNS("SNS")
        
        lambda_fn >> sns
        auth >> lambda_fn
        lambda_fn >> db

    with Cluster("CI/CD Pipeline"):
        gitlab = Gitlab("GitLab")
        pipeline = Cloudformation("Pipeline")
        
        gitlab >> pipeline
        pipeline >> app
        pipeline >> lambda_fn