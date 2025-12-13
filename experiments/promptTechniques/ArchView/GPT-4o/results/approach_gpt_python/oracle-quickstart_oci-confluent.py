from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.oci.database import ADB
from diagrams.onprem.network import Zookeeper
from diagrams.onprem.queue import Kafka

with Diagram("Confluent Platform Deployment on OCI", show=False):
    with Cluster("Oracle Cloud Infrastructure"):
        oci_adb = ADB("Autonomous DB")
        with Cluster("Confluent Platform"):
            zookeeper = Zookeeper("Zookeeper")
            kafka_broker = Kafka("Kafka Broker")
            schema_registry = Kafka("Schema Registry")
            rest_proxy = Kafka("REST Proxy")
            connect = Kafka("Connect")
            ksql = Kafka("KSQL")
            control_center = Kafka("Control Center")

            zookeeper >> kafka_broker
            kafka_broker >> schema_registry
            kafka_broker >> rest_proxy
            kafka_broker >> connect
            kafka_broker >> ksql
            kafka_broker >> control_center

        oci_adb << connect