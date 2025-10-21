from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Internet
from diagrams.generic.network import Firewall
from diagrams.generic.os import Ubuntu
from diagrams.oci.compute import Container
from diagrams.oci.network import LoadBalancer, NATGateway, ServiceGateway, VCN, Subnet
from diagrams.oci.general import User

with Diagram("OKE A1 Cluster Provisioning with Terraform", show=False):
    user = User("Administrator")

    internet = Internet("Internet")
    
    with Cluster("OCI"):
        vcn = VCN("Virtual Cloud Network")
        
        with Cluster("Subnets"):
            public_subnet = Subnet("Public Subnet")
            private_subnet = Subnet("Private Subnet")
        
        igw = Firewall("Internet Gateway")
        ngw = NATGateway("NAT Gateway")
        sgw = ServiceGateway("Service Gateway")
        
        with Cluster("OKE Cluster"):
            control_plane = Container("Control Plane")
            with Cluster("Node Pool"):
                worker_node1 = Ubuntu("Worker Node 1\nVM.Standard.A1.Flex")
                worker_node2 = Ubuntu("Worker Node 2\nVM.Standard.A1.Flex")
            
            kube_api = Firewall("Kubernetes API Endpoint")

        load_balancer = LoadBalancer("Load Balancer")
        nginx_app = Container("Nginx Application")

    user >> Edge(label="ssh") >> kube_api
    kube_api >> Edge(label="API Requests") >> control_plane
    control_plane >> Edge(label="Manage") >> [worker_node1, worker_node2]
    
    internet >> igw >> public_subnet
    private_subnet >> ngw >> internet
    private_subnet >> sgw >> vcn
    
    [worker_node1, worker_node2] >> load_balancer >> nginx_app
    nginx_app >> Edge(label="Expose Service") >> internet