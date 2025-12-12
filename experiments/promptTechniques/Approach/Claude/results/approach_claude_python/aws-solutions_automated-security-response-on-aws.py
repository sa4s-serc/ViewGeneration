from diagrams import Diagram, Cluster
from diagrams.aws.security import SecurityHub, Cognito, IAM, Macie 
from diagrams.aws.integration import StepFunctions, Eventbridge
from diagrams.aws.management import SystemsManager, Cloudwatch
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS
from diagrams.aws.database import Dynamodb

with Diagram("Automated Security Response Architecture", show=False):
    with Cluster("Security Controls"):
        securityhub = SecurityHub("Security Hub")
        macie = Macie("Security Findings")
        
    with Cluster("Core Components"):
        eventbridge = Eventbridge("Event Rules")
        stepfunctions = StepFunctions("Orchestrator") 
        ssm = SystemsManager("SSM Automation")
        
    with Cluster("Supporting Services"):
        lambda_fn = Lambda("Lambda Functions")
        cloudwatch = Cloudwatch("Monitoring & Logs")
        sqs = SQS("Throttling Queue")
        dynamo = Dynamodb("State Storage")
        s3 = S3("Artifacts")
        
    with Cluster("Authentication"):
        iam = IAM("IAM Roles")
        cognito = Cognito("Authentication")

    # Control Flow
    securityhub >> eventbridge >> stepfunctions
    macie >> securityhub
    
    stepfunctions >> ssm
    ssm >> lambda_fn
    lambda_fn >> sqs
    
    # Data Flow  
    lambda_fn >> dynamo
    lambda_fn >> s3
    lambda_fn >> cloudwatch
    
    # Auth Flow
    iam - lambda_fn
    iam - ssm
    cognito - lambda_fn