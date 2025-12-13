from diagrams import Diagram, Cluster, Edge
from diagrams.oci.compute import OKE, ContainerEngine, Container
from diagrams.oci.network import Vcn, InternetGateway, RouteTable, SecurityLists, LoadBalancer, ServiceGateway
from diagrams.onprem.network import Nginx
from diagrams.onprem.iac import Terraform
from diagrams.k8s.network import Ingress

with Diagram("OKE A1 Cluster Provisioning with Terraform", show=False):
    terraform = Terraform("Terraform Configuration")

    with Cluster("OCI Infrastructure"):
        vcn = Vcn("Virtual Cloud Network")
        internet_gateway = InternetGateway("Internet Gateway")
        service_gateway = ServiceGateway("Service Gateway")
        route_table = RouteTable("Route Table")
        security_lists = SecurityLists("Security Lists")

        with Cluster("Subnets"):
            public_subnet = Vcn("Public Subnet")
            private_subnet = Vcn("Private Subnet")

        load_balancer = LoadBalancer("Load Balancer")

    with Cluster("OKE Cluster"):
        oke = OKE("OKE")
        container_engine = ContainerEngine("Container Engine")
        
        with Cluster("Node Pool"):
            container = Container("Ampere A1 Nodes")

    nginx = Nginx("Nginx Deployment")
    ingress = Ingress("Ingress")

    terraform >> vcn
    vcn >> Edge(label="Route") >> internet_gateway
    vcn >> Edge(label="Route") >> service_gateway
    vcn >> Edge(label="Route") >> route_table
    vcn >> Edge(label="Security") >> security_lists

    public_subnet >> Edge(label="Connected to") >> internet_gateway
    private_subnet >> Edge(label="Connected to") >> service_gateway
    load_balancer >> Edge(label="Connected to") >> public_subnet

    oke >> Edge(label="Runs on") >> container_engine
    container_engine >> Edge(label="Manages") >> container

    load_balancer >> Edge(label="Distributes to") >> nginx
    nginx >> Edge(label="Exposed via") >> ingress