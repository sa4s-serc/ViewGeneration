from diagrams import Diagram, Cluster, Node
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.k8s.storage import PV
from diagrams.onprem.analytics import Spark
from diagrams.onprem.storage import HDFS

with Diagram("K8s Big Data Architecture", show=False, direction="TB"):
    with Cluster("Kubernetes Cluster"):
        with Cluster("Apache Hadoop"):
            namenode = HDFS("NameNode")
            datanode = [HDFS("DataNode1"),
                        HDFS("DataNode2"),
                        HDFS("DataNode3")]
            
        with Cluster("Apache Spark"):
            spark_master = Spark("Spark Master")
            spark_worker = [Spark("Spark Worker1"),
                            Spark("Spark Worker2"),
                            Spark("Spark Worker3")]

        with Cluster("HiBench Benchmark Suite"):
            hibench = Node("HiBench")

        kubernetes_services = Service("K8s Services")

    with Cluster("Kubernetes Deployment"):
        hadoop_pvc = PV("HDFS Storage")
        k8s_pods = Pod("K8s Pods")

    hibench << spark_master
    spark_master << spark_worker
    spark_master >> namenode
    namenode >> datanode

    kubernetes_services << [namenode, spark_master, hibench]
    k8s_pods << [hadoop_pvc, kubernetes_services]