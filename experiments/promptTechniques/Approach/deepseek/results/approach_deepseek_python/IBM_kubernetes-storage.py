from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.storage import PV, PVC, StorageClass
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.podconfig import ConfigMap, Secret
from diagrams.onprem.database import MongoDB
from diagrams.onprem.storage import Ceph
from diagrams.aws.storage import S3
from diagrams.ibm.storage import BlockStorage

with Diagram("Kubernetes Storage Workshop Architecture", show=False, direction="LR"):
    ingress = Ingress("Ingress")
    frontend = Pod("Guestbook Frontend")
    backend = Pod("Guestbook Backend")
    mongodb = MongoDB("MongoDB")
    
    with Cluster("Storage Solutions"):
        non_persistent = StorageClass("Non-Persistent")
        file_storage = PV("File Storage")
        block_storage = BlockStorage("Block Storage")
        object_storage = S3("Object Storage")
        sds_storage = Ceph("SDS Storage")
        external_storage = PV("External Storage")
    
    config = ConfigMap("ConfigMap")
    secret = Secret("Secret")
    
    ingress >> frontend
    frontend >> backend
    backend >> mongodb
    
    frontend >> non_persistent
    backend >> file_storage
    mongodb >> block_storage
    backend >> object_storage
    backend >> sds_storage
    backend >> external_storage
    
    config >> frontend
    config >> backend
    secret >> frontend
    secret >> backend