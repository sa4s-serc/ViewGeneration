from diagrams import Diagram, Cluster
from diagrams.aws.analytics import Kinesis
from diagrams.aws.storage import S3
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.compute import Server
from diagrams.programming.framework import Django
from diagrams.aws.ml import Sagemaker
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.analytics import Spark
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Internet

with Diagram("Real-Time Streaming Analytics System for Stock Price Prediction", show=False, direction="TB"):
    internet = Internet("Internet")

    with Cluster("Data Ingestion"):
        twitter_service = Server("Twitter Service")
        iex_service = Server("IEX Service")
        manager_service = Server("Manager Service")
        kinesis = Kinesis("AWS Kinesis")

    with Cluster("Data Storage"):
        mongodb = MongoDB("MongoDB")
        redis = Redis("Redis")
        s3 = S3("S3 Storage")

    with Cluster("Data Processing"):
        spark = Spark("Spark Processing")
        airflow = Airflow("Airflow Scheduler")

    with Cluster("Data Analysis"):
        sklearn_model_dev = Sagemaker("SKLearn Model Development")
        sklearn_model_deploy = Sagemaker("SKLearn Model Deployment")
        eda = Server("Exploratory Data Analysis")

    with Cluster("Data Service"):
        django_api = Django("Django REST API")

    with Cluster("Infrastructure"):
        docker = Docker("Docker Containers")

    internet >> [twitter_service, iex_service]
    [twitter_service, iex_service] >> kinesis
    manager_service >> redis
    kinesis >> spark
    spark >> [mongodb, redis, s3]
    airflow >> [sklearn_model_dev, sklearn_model_deploy]
    sklearn_model_dev >> s3
    sklearn_model_deploy >> [mongodb, redis]
    eda >> mongodb
    django_api >> mongodb
    docker - [twitter_service, iex_service, manager_service, spark, airflow, sklearn_model_dev, sklearn_model_deploy, eda, django_api]