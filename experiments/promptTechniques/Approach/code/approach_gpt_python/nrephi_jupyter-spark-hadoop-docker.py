from diagrams import Diagram
from diagrams.custom import Custom
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import MySQL, PostgreSQL
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Users
from diagrams.onprem.inmemory import Hadoop
from diagrams.programming.language import Python, R
from diagrams.generic.os import Centos

with Diagram("Dockerized Jupyter Spark Standalone Cluster", show=False):
    jupyterlab = Custom("JupyterLab", "./resources/jupyterlab.png")
    spark_master = Spark("Spark Master")
    spark_worker = Spark("Spark Worker")
    mysql = MySQL("MySQL (Hue)")
    hadoop_namenode = Hadoop("Hadoop NameNode")
    hadoop_datanode = Hadoop("Hadoop DataNode")
    hive_metastore = PostgreSQL("Hive Metastore")
    hive_server = Custom("Hive Server", "./resources/hive.png")
    hue_interface = Custom("Hue Interface", "./resources/hue.png")
    user = Users("Developer")

    user >> jupyterlab
    jupyterlab - [spark_master, spark_worker]
    spark_master - spark_worker
    hue_interface - mysql
    hadoop_namenode - hadoop_datanode
    hive_server - hive_metastore

    jupyterlab >> [Python("PySpark"), R("SparkR")]
    hadoop_namenode >> hive_server
    hue_interface >> hive_server
    mysql >> hue_interface
    jupyterlab >> Centos("Docker Environment")