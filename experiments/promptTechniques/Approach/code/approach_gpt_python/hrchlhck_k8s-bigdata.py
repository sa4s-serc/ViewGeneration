from diagrams import Diagram
from diagrams.k8s.compute import Pod, Deployment, StatefulSet
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.storage import PV, PVC
from diagrams.onprem.analytics import Spark, Hadoop
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Istio

with Diagram("Kubernetes Big Data Architecture", show=False):
    ingress = Ingress("ingress")
    service = Service("service")

    spark_master = Spark("Spark Master")
    spark_worker = Spark("Spark Worker")
    hadoop_namenode = Hadoop("Hadoop NameNode")
    hadoop_datanode = Hadoop("Hadoop DataNode")
    kafka = Kafka("Kafka")

    statefulset = StatefulSet("StatefulSet")
    deployment = Deployment("Deployment")

    pv = PV("Persistent Volume")
    pvc = PVC("Persistent Volume Claim")

    prometheus = Prometheus("Prometheus")
    istio = Istio("Istio")

    ingress >> service >> [spark_master, hadoop_namenode]
    spark_master >> spark_worker
    hadoop_namenode >> hadoop_datanode
    statefulset >> pvc >> pv
    deployment >> service
    [spark_master, hadoop_namenode] >> kafka
    prometheus >> [spark_master, hadoop_namenode, kafka]
    istio >> ingress