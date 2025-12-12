from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda, ECS, EKS
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import ELB, CloudFront, Route53
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis, EMR
from diagrams.aws.ml import Sagemaker
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import User
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python
from diagrams.generic.database import SQL

with Diagram("MLOps LEGO Minifigure Classification Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Data Sources"):
        kaggle = SQL("Kaggle Dataset")
        s3_raw = S3("Raw Data S3")
    
    with Cluster("Data Processing"):
        with Cluster("Data Ingestion"):
            get_data = Python("get_data.py")
            data_exploration = Python("data_feeling.ipynb")
        
        with Cluster("Model Training"):
            train_model = Python("train_model.py")
            mlflow_tracking = Sagemaker("MLflow Tracking")
            model_registry = Sagemaker("MLflow Registry")
    
    with Cluster("Model Serving"):
        with Cluster("Batch Prediction"):
            batch_service = ECS("Batch Service")
            prefect_flow = Airflow("Prefect Flow")
        
        with Cluster("Stream Prediction"):
            stream_service = EKS("Stream Service")
            stream_simulator = Python("streaming_send_data.py")
    
    with Cluster("Monitoring"):
        evidently = Prometheus("Evidently")
        grafana = Grafana("Grafana")
        cloudwatch = Cloudwatch("CloudWatch")
    
    with Cluster("Infrastructure"):
        docker = Docker("Docker")
        docker_compose = Docker("Docker Compose")
        nginx = ELB("Nginx")
    
    with Cluster("CI/CD"):
        github_actions = Python("GitHub Actions")
        pre_commit = Python("Pre-commit")
        tests = Python("Unit/Integration Tests")
    
    # Data flow connections
    kaggle >> get_data >> s3_raw
    s3_raw >> data_exploration
    s3_raw >> train_model >> mlflow_tracking >> model_registry
    
    # Model serving connections
    model_registry >> batch_service
    model_registry >> stream_service
    prefect_flow >> batch_service
    stream_simulator >> stream_service
    
    # Monitoring connections
    batch_service >> evidently
    stream_service >> evidently
    evidently >> grafana
    evidently >> cloudwatch
    
    # User interactions
    user >> batch_service
    user >> stream_service
    
    # Infrastructure connections
    docker >> batch_service
    docker >> stream_service
    docker_compose >> nginx
    nginx >> mlflow_tracking
    
    # CI/CD connections
    github_actions >> tests
    pre_commit >> tests
    tests >> docker
    tests >> docker_compose