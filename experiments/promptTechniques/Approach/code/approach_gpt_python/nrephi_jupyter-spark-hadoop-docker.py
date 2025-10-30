from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import MySQL, PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.queue import Kafka
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.network import Nginx
from diagrams.onprem.vcs import Git
from diagrams.programming.language import Python

with Diagram("Dockerized Jupyter Spark Standalone Cluster", show=False):
    git = Git("GitHub Repo")

    with Cluster("Dockerized Environment"):
        jupyter = Python("JupyterLab")
        spark_master = Spark("Spark Master")
        spark_worker1 = Spark("Spark Worker 1")
        spark_worker2 = Spark("Spark Worker 2")

        git >> jupyter
        jupyter >> [spark_master, spark_worker1, spark_worker2]

        with Cluster("Hadoop Ecosystem"):
            namenode = Server("Hadoop NameNode")
            datanode = Server("Hadoop DataNode")
            hive_metastore = MySQL("Hive Metastore")
            hive_server = Server("Hive Server")
            hue = Server("Hue")
            mysql_hue = MySQL("Hue MySQL")

            [namenode, datanode] - hive_metastore
            hive_metastore >> hive_server
            hue >> mysql_hue
            hue - [hive_server, namenode]

        with Cluster("Monitoring"):
            prometheus = Prometheus("Prometheus")
            grafana = Grafana("Grafana")

        with Cluster("Messaging & Workflow"):
            kafka = Kafka("Kafka")
            airflow = Airflow("Airflow")

        with Cluster("Additional Services"):
            nginx = Nginx("Nginx")
            redis = Redis("Redis")
            postgres = PostgreSQL("PostgreSQL")

        [spark_master, spark_worker1, spark_worker2] >> kafka
        for sm in [spark_master, spark_worker1, spark_worker2]:
            sm >> prometheus
            sm >> grafana
        nginx >> [jupyter, hue]
        [kafka, airflow] >> postgres