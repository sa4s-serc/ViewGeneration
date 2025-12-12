from diagrams import Diagram, Cluster
from diagrams.aws.analytics import Redshift, Glue, Kinesis
from diagrams.aws.storage import S3
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.analytics import Spark
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS

with Diagram("Movalytics Data Warehouse Architecture", show=False, direction="LR"):
    with Cluster("Data Sources"):
        kaggle = S3("Kaggle MovieLens")
        fred = S3("St. Louis FRED CPI")

    with Cluster("Orchestration & Containerization"):
        airflow = Airflow("Apache Airflow")
        docker = Docker("Docker")

    with Cluster("Data Processing"):
        spark = Spark("Apache Spark")
        python_scripts = Python("Python Scripts")

    with Cluster("Data Warehouse"):
        redshift = Redshift("Amazon Redshift")
        staging_tables = RDS("Staging Tables")
        dim_tables = RDS("Dimension Tables")

    with Cluster("Data Quality"):
        dq_operator = Lambda("DataQualityOperator")

    kaggle >> airflow
    fred >> airflow
    airflow >> spark
    airflow >> python_scripts
    spark >> staging_tables
    python_scripts >> staging_tables
    staging_tables >> dq_operator
    dq_operator >> dim_tables
    docker >> airflow