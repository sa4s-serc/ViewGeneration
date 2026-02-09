from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, StatefulSet
from diagrams.k8s.network import Service
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Hbase
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Python

with Diagram("Kubernetes Big Data Architecture", show=False, direction="TB"):
    with Cluster("Kubernetes Cluster"):
        master_node = Pod("Master Node")
        
        with Cluster("Hadoop Cluster"):
            namenode = Hbase("NameNode")
            resourcemanager = Hbase("ResourceManager")
            historyserver = Hbase("HistoryServer")
            
            with Cluster("DataNodes"):
                datanodes = StatefulSet("DataNodes")
                datanode1 = Pod("DataNode1")
                datanode2 = Pod("DataNode2")
                datanode3 = Pod("DataNode3")
                
        with Cluster("Spark Cluster"):
            spark_master = Spark("Spark Master")
            spark_workers = Spark("Spark Workers")
            
        with Cluster("HiBench"):
            hibench = Airflow("HiBench Suite")
            
        with Cluster("Configuration"):
            config_scripts = Python("Config Scripts")
            env_vars = Python("Environment Variables")
    
    master_node >> namenode
    master_node >> resourcemanager
    master_node >> historyserver
    master_node >> spark_master
    
    namenode >> datanodes
    resourcemanager >> datanodes
    datanode1 >> datanode2
    datanode2 >> datanode3
    
    spark_master >> spark_workers
    spark_workers >> datanodes
    
    hibench >> namenode
    hibench >> spark_master
    
    config_scripts >> namenode
    config_scripts >> resourcemanager
    config_scripts >> historyserver
    config_scripts >> datanodes
    config_scripts >> spark_master
    config_scripts >> spark_workers
    
    env_vars >> config_scripts