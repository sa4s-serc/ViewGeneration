from diagrams import Diagram, Cluster
from diagrams.oci.compute import VirtualMachine
from diagrams.oci.database import Autonomous
from diagrams.oci.storage import ObjectStorage
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Zookeeper
from diagrams.oci.network import LoadBalancer
from diagrams.oci.security import Vault

with Diagram("Confluent Platform on OCI Architecture", show=False, direction="TB"):
    lb = LoadBalancer("Load Balancer")
    
    with Cluster("Confluent Platform"):
        zk = Zookeeper("Zookeeper")
        
        with Cluster("Kafka Cluster"):
            kafka_broker1 = Kafka("Broker 1")
            kafka_broker2 = Kafka("Broker 2")
            kafka_broker3 = Kafka("Broker 3")
        
        with Cluster("Confluent Services"):
            schema_registry = VirtualMachine("Schema Registry")
            rest_proxy = VirtualMachine("REST Proxy")
            ksql = VirtualMachine("KSQL")
            connect = VirtualMachine("Connect")
            control_center = VirtualMachine("Control Center")
    
    with Cluster("Oracle Cloud Services"):
        adb = Autonomous("Autonomous Database")
        object_storage = ObjectStorage("Object Storage")
        security = Vault("Security Vault")
    
    lb >> [kafka_broker1, kafka_broker2, kafka_broker3]
    zk >> [kafka_broker1, kafka_broker2, kafka_broker3]
    [kafka_broker1, kafka_broker2, kafka_broker3] >> schema_registry
    [kafka_broker1, kafka_broker2, kafka_broker3] >> rest_proxy
    [kafka_broker1, kafka_broker2, kafka_broker3] >> ksql
    [kafka_broker1, kafka_broker2, kafka_broker3] >> connect
    [kafka_broker1, kafka_broker2, kafka_broker3] >> control_center
    connect >> adb
    connect >> object_storage
    security - adb
    security - object_storage
    security - kafka_broker1
    security - kafka_broker2
    security - kafka_broker3