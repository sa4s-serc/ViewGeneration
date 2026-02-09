from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, DaemonSet
from diagrams.k8s.network import Service
from diagrams.k8s.storage import PV, PVC
from diagrams.k8s.infra import Master
from diagrams.k8s.others import CRD
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Go

with Diagram("Kubescape Host Scanner Architecture", show=False):
    with Cluster("Kubernetes Cluster"):
        master = Master("Control Plane")
        
        with Cluster("Host Scanner Components"):
            daemonset = DaemonSet("Host Scanner")
            api = Service("HTTP API")
            storage = PV("Host Data")
            storage_claim = PVC("Storage Claim")
            
            # Custom resources
            crd = CRD("Scanner CRD")
            
            # Monitoring components
            prometheus = Prometheus("Metrics")
            
            # External components
            nginx = Nginx("Ingress")
            
            # Core application
            app = Go("Scanner Logic")
            
            # Flow
            master >> crd
            crd >> daemonset
            daemonset >> app
            app >> storage_claim
            storage_claim >> storage
            app >> api
            api >> nginx
            app >> prometheus