from diagrams import Diagram, Cluster
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.workflow import Airflow
from diagrams.programming.framework import FastAPI
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.generic.database import SQL
from diagrams.generic.compute import Rack
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.device import Mobile

with Diagram("Feature Hero ML - Feature Store Architecture", show=False, direction="TB"):
    with Cluster("Data Sources"):
        external_data = Storage("External Data")
    
    with Cluster("Data Ingestion Layer"):
        data_fetch = Python("fetch_card_transdata.py")
        data_transform = Python("Data Transformation")
        data_split = Python("get_train_val_card_transdata.py")
        
        external_data >> data_fetch >> data_transform >> data_split
    
    with Cluster("Feature Store Core"):
        feast_core = Rack("Feast Framework")
        feature_definitions = Python("card_transdata_feature_definition.py")
        dataset_creation = Python("fetch_train_val_dataset_card_transdata.py")
        
        data_split >> dataset_creation >> feast_core
        feature_definitions >> feast_core
    
    with Cluster("Storage Layer"):
        with Cluster("Online Store"):
            redis = Redis("Redis")
        
        with Cluster("Offline Store"):
            parquet = Storage("Parquet Files")
            minio = PostgreSQL("MinIO")
            
        feast_core >> redis
        feast_core >> parquet
        parquet >> minio
    
    with Cluster("Serving Layer"):
        feature_server = FastAPI("Feature Server")
        redis >> feature_server
    
    with Cluster("Consumers"):
        training = LinuxGeneral("Model Training")
        inference = Mobile("Real-time Inference")
        
        feature_server >> training
        feature_server >> inference
    
    with Cluster("Infrastructure"):
        docker = LinuxGeneral("Docker")
        compose = LinuxGeneral("Docker Compose")
        
        docker >> compose
    
    with Cluster("Development Tools"):
        pre_commit = Python("pre-commit hooks")
        tests = Python("Unit Tests")