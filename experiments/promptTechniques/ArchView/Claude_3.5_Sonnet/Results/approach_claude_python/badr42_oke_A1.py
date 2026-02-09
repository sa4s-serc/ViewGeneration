from diagrams import Diagram, Cluster
from diagrams.oci.compute import OKE, Container
from diagrams.oci.network import Vcn, RouteTable, SecurityLists
from diagrams.oci.connectivity import CustomerPremises
from diagrams.k8s.compute import Pod, Deploy 
from diagrams.k8s.network import Service
from diagrams.oci.governance import Compartments
from diagrams.oci.storage import ObjectStorage
from diagrams.oci.network import ServiceGateway
from diagrams.oci.network import InternetGatewayWhite

with Diagram("OKE A1 Cluster Architecture", show=False):
    with Cluster("OCI Cloud"):
        with Cluster("Compartment"):
            comp = Compartments("Compartment")
            
            with Cluster("Virtual Cloud Network"):
                vcn = Vcn("VCN")
                igw = InternetGatewayWhite("Internet Gateway")
                sgw = ServiceGateway("Service Gateway")
                rt = RouteTable("Route Tables")
                sl = SecurityLists("Security Lists")
                
                vcn >> igw
                vcn >> sgw
                vcn >> rt
                vcn >> sl

            with Cluster("OKE Cluster"):
                oke = OKE("OKE Cluster")
                
                with Cluster("Node Pool"):
                    with Cluster("Worker Nodes"):
                        pods = [Pod("Nginx Pod") for _ in range(3)]
                    
                    deploy = Deploy("Nginx Deployment")
                    svc = Service("Load Balancer")
                    
                    deploy >> pods
                    svc >> pods

            storage = ObjectStorage("Object Storage")
            
            comp >> vcn
            comp >> oke
            oke >> vcn

    client = CustomerPremises("Client")
    client >> igw