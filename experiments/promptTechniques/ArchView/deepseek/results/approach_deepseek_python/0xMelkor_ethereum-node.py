from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.storage import PersistentVolumeClaim
from diagrams.k8s.network import Service, Ingress
from diagrams.onprem.database import InfluxDB
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import User
from diagrams.gcp.devtools import Build

with Diagram("Ethereum Node Deployment on GKE", show=False, direction="TB"):
    user = User("External User")
    
    with Cluster("Google Cloud Build CI/CD"):
        cloudbuild = Build("Cloud Build")
    
    with Cluster("GKE Cluster"):
        with Cluster("Nginx Reverse Proxy"):
            nginx = Nginx("Nginx")
            ingress = Ingress("Ingress")
        
        with Cluster("Ethereum Node"):
            with Cluster("Geth Execution Layer"):
                geth_pod = Pod("Geth Pod")
                geth_pvc = PersistentVolumeClaim("Geth PVC (2000Gi)")
                geth_service = Service("Geth Service")
            
            with Cluster("Lighthouse Consensus Layer"):
                lighthouse_pod = Pod("Lighthouse Pod")
                lighthouse_pvc = PersistentVolumeClaim("Lighthouse PVC (500Gi)")
                lighthouse_service = Service("Lighthouse Service")
        
        with Cluster("Monitoring"):
            influxdb = InfluxDB("InfluxDB")
            influxdb_pvc = PersistentVolumeClaim("InfluxDB PVC")
            influxdb_service = Service("InfluxDB Service")
    
    # Connections
    cloudbuild >> [geth_pod, lighthouse_pod, nginx, influxdb]
    
    user >> ingress >> nginx
    nginx >> [geth_service, influxdb_service]
    
    geth_service >> geth_pod
    lighthouse_service >> lighthouse_pod
    influxdb_service >> influxdb
    
    geth_pod >> geth_pvc
    lighthouse_pod >> lighthouse_pvc
    influxdb >> influxdb_pvc
    
    geth_pod >> influxdb
    lighthouse_pod >> geth_pod