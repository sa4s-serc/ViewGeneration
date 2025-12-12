from diagrams import Diagram, Cluster
from diagrams.oci.compute import OKE, ContainerEngine
from diagrams.oci.network import InternetGateway, ServiceGateway, LoadBalancer
from diagrams.oci.database import Autonomous
from diagrams.oci.storage import ObjectStorage
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import User
from diagrams.oci.security import CloudGuard
from diagrams.oci.monitoring import Alarm

with Diagram("OKE A1 Cluster Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("VCN"):
        internet_gateway = InternetGateway("Internet Gateway")
        nat_gateway = InternetGateway("NAT Gateway")
        service_gateway = ServiceGateway("Service Gateway")
        load_balancer = LoadBalancer("Load Balancer")
        
        with Cluster("Subnets"):
            with Cluster("Public Subnet"):
                control_plane = OKE("Control Plane")
            
            with Cluster("Private Subnet"):
                worker_nodes = OKE("Worker Nodes\n(VM.Standard.A1.Flex)")
    
    oke_cluster = ContainerEngine("OKE Cluster")
    nginx = Nginx("Nginx Application")
    terraform = ObjectStorage("Terraform Config")
    monitoring = Alarm("Monitoring")
    security = CloudGuard("Security")
    
    user >> internet_gateway
    internet_gateway >> control_plane
    internet_gateway >> load_balancer
    
    control_plane >> worker_nodes
    worker_nodes >> nginx
    load_balancer >> nginx
    
    worker_nodes >> nat_gateway
    worker_nodes >> service_gateway
    
    terraform >> oke_cluster
    monitoring >> oke_cluster
    monitoring >> nginx
    security >> oke_cluster