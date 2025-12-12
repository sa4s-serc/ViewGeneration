from diagrams import Diagram, Cluster
from diagrams.onprem.analytics import Spark, Hadoop
from diagrams.onprem.container import Docker
from diagrams.onprem.database import MySQL, PostgreSQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.client import Users

with Diagram("Dockerized Jupyter Spark Hadoop Cluster", show=False):

    with Cluster("Docker Environment"):
        docker = Docker("Docker")

        with Cluster("Compute Layer"):
            with Cluster("Spark Cluster"):
                master = Spark("Spark Master")
                worker1 = Spark("Spark Worker 1") 
                worker2 = Spark("Spark Worker 2")
                master >> worker1
                master >> worker2

            with Cluster("Hadoop Cluster"):
                hadoop = Hadoop("Hadoop")
                namenode = Hadoop("NameNode")
                datanode = Hadoop("DataNode") 
                hadoop >> namenode
                hadoop >> datanode

        with Cluster("Storage Layer"):
            mysql = MySQL("MySQL\n(Hue Metadata)")
            postgres = PostgreSQL("PostgreSQL\n(Hive Metastore)")
            kafka = Kafka("Message Queue")

        # Connect components
        worker1 >> mysql
        worker1 >> postgres 
        worker1 >> kafka
        worker2 >> mysql
        worker2 >> postgres
        worker2 >> kafka
        
        worker1 >> hadoop
        worker2 >> hadoop

        # Docker orchestrates everything
        docker >> master
        docker >> hadoop
        docker >> mysql
        docker >> postgres
        docker >> kafka