from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.onprem.client import User
from diagrams.oracle.compute import OciCompute
from diagrams.generic.storage import Storage

with Diagram("Confluent Platform on OCI", show=False, direction="TB"):
    user = User("Client")

    with Cluster("Oracle Cloud Infrastructure (OCI)"):
        internet = Internet("Internet Gateway")
        
        with Cluster("Network Components"):
            vcn = OciCompute("Virtual Cloud Network")
            subnet = OciCompute("Subnets")
            security_list = OciCompute("Security Lists")

        with Cluster("Confluent Platform Deployment"):
            zookeeper = Server("Zookeeper")
            kafka_broker = Server("Kafka Broker")
            schema_registry = Server("Schema Registry")
            rest_proxy = Server("REST Proxy")
            connect = Server("Kafka Connect")
            ksql = Server("KSQL")
            control_center = Server("Control Center")

        with Cluster("OCI Services"):
            object_storage = Storage("Oracle Object Storage")
            adw = Storage("Autonomous Data Warehouse")
            atp = Storage("Autonomous Transaction Processing")

    user >> internet >> vcn >> subnet >> security_list
    security_list >> zookeeper
    security_list >> kafka_broker
    security_list >> schema_registry
    security_list >> rest_proxy
    security_list >> connect
    security_list >> ksql
    security_list >> control_center

    connect >> object_storage
    connect >> adw
    connect >> atp