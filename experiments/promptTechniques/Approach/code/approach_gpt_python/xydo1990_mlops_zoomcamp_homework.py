from diagrams import Diagram, Cluster, Edge
from diagrams.generic.os import Ubuntu
from diagrams.onprem.workflow import Prefect
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.analytics import Jupyter
from diagrams.onprem.database import MongoDB
from diagrams.onprem.vcs import Github
from diagrams.generic.storage import Storage
from diagrams.programming.flowchart import Action
from diagrams.onprem.mlops import Mlflow

with Diagram("MLOps Project for LEGO Minifigure Classification", show=False):
    github = Github("GitHub Repo")
    
    with Cluster("Data Exploration"):
        data_exploration = Jupyter("data_feeling.ipynb")
        
    with Cluster("Model Training"):
        get_data = Action("get_data.py")
        train_model = Action("train_model.py")
        mlflow = Mlflow("MLflow")
        model_registry = Storage("Model Registry")
        
    with Cluster("Model Deployment"):
        docker_batch = Docker("Batch Service")
        docker_stream = Docker("Streaming Service")
        mlflow_container = Docker("MLflow Container")
        nginx = Ubuntu("Nginx")
        
    with Cluster("Workflow Orchestration"):
        prefect = Prefect("Prefect")
        
    with Cluster("Model Monitoring"):
        evidently = Action("Evidently")
        monitoring_config = Storage("Monitoring Configs")
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        
    with Cluster("Testing & Code Quality"):
        unit_tests = Action("Unit Tests")
        integration_tests = Action("Integration Tests")
        pre_commit = Action("Pre-Commit Hooks")
        
    github >> data_exploration
    github >> get_data >> train_model >> mlflow >> model_registry
    model_registry - Edge(label="Promote Model") >> docker_batch
    model_registry - Edge(label="Promote Model") >> docker_stream
    docker_batch >> nginx
    docker_stream >> nginx
    prefect >> docker_batch
    evidently >> monitoring_config
    evidently >> prometheus
    prometheus >> grafana
    github >> unit_tests
    github >> integration_tests
    github >> pre_commit
    mlflow_container >> mlflow
    mongodb = MongoDB("MongoDB")
    mlflow_container >> mongodb
    github >> mlflow_container
    github >> nginx