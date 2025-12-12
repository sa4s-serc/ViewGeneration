from diagrams import Diagram, Cluster
from diagrams.aws.ml import Sagemaker, SagemakerNotebook, SagemakerTrainingJob, SagemakerModel, SagemakerGroundTruth
from diagrams.aws.analytics import Athena, Glue, GlueDataCatalog, LakeFormation
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SNS, SQS, StepFunctions
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.mlops import Mlflow
from diagrams.generic.blank import Blank

with Diagram("SageMaker ML Architecture", show=False, direction="TB"):
    with Cluster("Data Layer"):
        s3 = S3("S3 Bucket")
        glue_catalog = GlueDataCatalog("Glue Data Catalog")
        athena = Athena("Athena")
        lake_formation = LakeFormation("Lake Formation")
        dynamodb = Dynamodb("DynamoDB")
        
    with Cluster("Training Pipeline"):
        with Cluster("Data Preparation"):
            ground_truth = SagemakerGroundTruth("Ground Truth")
            glue = Glue("Glue ETL")
            
        with Cluster("Model Development"):
            notebook = SagemakerNotebook("SageMaker Notebook")
            training_job = SagemakerTrainingJob("Training Job")
            huggingface = Blank("Hugging Face")
            mlflow = Mlflow("MLflow")
            
    with Cluster("Deployment & Inference"):
        model = SagemakerModel("SageMaker Model")
        endpoint = Sagemaker("SageMaker Endpoint")
        
    with Cluster("Orchestration & Monitoring"):
        step_functions = StepFunctions("Step Functions")
        sns = SNS("SNS")
        sqs = SQS("SQS")
        cloudwatch = Cloudwatch("CloudWatch")
        iam = IAM("IAM")
    
    s3 >> glue >> glue_catalog
    glue_catalog >> athena
    lake_formation >> glue_catalog
    s3 >> ground_truth
    ground_truth >> notebook
    notebook >> training_job
    huggingface >> training_job
    training_job >> mlflow
    mlflow >> model
    model >> endpoint
    step_functions >> training_job
    step_functions >> model
    sns >> step_functions
    sqs >> step_functions
    cloudwatch >> step_functions
    iam >> [training_job, model, endpoint]
    dynamodb >> notebook
    endpoint >> dynamodb