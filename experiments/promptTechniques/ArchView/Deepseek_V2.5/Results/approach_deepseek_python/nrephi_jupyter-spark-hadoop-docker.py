from diagrams import Diagram, Cluster
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL, MySQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Internet
from diagrams.onprem.analytics import Hadoop
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.client import User

with Diagram("Dockerized Jupyter Spark Standalone Cluster", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Spark Cluster"):
        jupyterlab = Spark("JupyterLab")
        spark_master = Spark("Spark Master")
        with Cluster("Spark Workers"):
            workers = [Spark("Worker 1"), Spark("Worker 2")]
    
    with Cluster("Hadoop Ecosystem"):
        namenode = Hadoop("NameNode")
        datanode = Hadoop("DataNode")
        hive_server = Hadoop("Hive Server")
        with Cluster("Hive Metastore"):
            postgresql = PostgreSQL("PostgreSQL")
        hue = Hadoop("Hue")
        mysql = MySQL("MySQL")
    
    user >> jupyterlab
    jupyterlab >> spark_master
    spark_master >> workers
    jupyterlab >> namenode
    namenode >> datanode
    jupyterlab >> hive_server
    hive_server >> postgresql
    hue >> mysql
    hue >> namenode