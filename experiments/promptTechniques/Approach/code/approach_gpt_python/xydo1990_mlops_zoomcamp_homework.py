from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECR
from diagrams.aws.ml import Sagemaker
from diagrams.onprem.mlops import Mlflow
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.generic.os import Ubuntu
from diagrams.onprem.workflow import Airflow
from diagrams.aws.devtools import Codebuild
from diagrams.firebase.develop import Authentication
from diagrams.onprem.database import PostgreSQL

with Diagram("MLOps Architecture for LEGO Minifigure Classification", show=False):
    with Cluster("Data Exploration"):
        data_exploration = Ubuntu("Jupyter Notebooks")

    with Cluster("Model Training"):
        get_data = Terraform("get_data.py")
        train_model = Codebuild("train_model.py")
        mlflow = Mlflow("MLflow")

    with Cluster("Experiment Tracking & Model Registry"):
        experiment_tracking = Sagemaker("Experiments")
        model_registry = Sagemaker("Model Registry")

    with Cluster("Model Deployment"):
        docker = Docker("Docker")
        ecr = ECR("ECR")

    with Cluster("Workflow Orchestration"):
        prefect = Airflow("Prefect")

    with Cluster("Model Monitoring"):
        monitoring = Prometheus("Evidently")
        grafana_dashboard = Grafana("Grafana")

    with Cluster("Batch and Stream Serving"):
        batch_serving = Docker("Batch Prediction")
        stream_serving = Docker("Streaming Prediction")

    with Cluster("Testing & CI/CD"):
        github_actions = GithubActions("GitHub Actions")

    with Cluster("Artifact Storage"):
        storage = Authentication("AWS S3")

    with Cluster("Database"):
        db = PostgreSQL("PostgreSQL")

    data_exploration >> get_data >> train_model >> mlflow
    mlflow >> experiment_tracking >> model_registry
    model_registry >> docker >> [batch_serving, stream_serving]
    [batch_serving, stream_serving] >> monitoring >> grafana_dashboard
    docker >> storage
    train_model >> ecr
    github_actions >> docker
    prefect >> batch_serving
    storage >> db