from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, Deployment, StatefulSet
from diagrams.k8s.network import Service
from diagrams.k8s.storage import PV, PVC
from diagrams.k8s.infra import Master
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import Cassandra

with Diagram("K8s Big Data Architecture", show=False):
    with Cluster("Kubernetes Cluster"):
        master = Master("K8s Master")
        
        with Cluster("Processing Layer"):
            spark_master = Pod("Spark Master")
            spark_workers = [Pod("Spark Worker") for _ in range(2)]
            spark_master >> spark_workers
        
        with Cluster("Storage Layer"):
            hdfs_nn = StatefulSet("HDFS NameNode")
            hdfs_dn = [StatefulSet("HDFS DataNode") for _ in range(2)]
            hdfs_nn >> hdfs_dn
        
        with Cluster("Services"):
            namenode_svc = Service("NameNode Service")
            spark_svc = Service("Spark Service")
            
            namenode_svc >> hdfs_nn
            spark_svc >> spark_master
        
        with Cluster("Storage"):
            pv = PV("Persistent Volume")
            pvc = PVC("Volume Claim")
            pv >> pvc
            pvc >> hdfs_dn
        
        master >> [namenode_svc, spark_svc]