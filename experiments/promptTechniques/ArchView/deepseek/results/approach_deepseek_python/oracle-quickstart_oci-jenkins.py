from diagrams import Diagram
from diagrams.oci.compute import VM
from diagrams.oci.network import LoadBalancer, Vcn, InternetGateway, RouteTable, SecurityLists
from diagrams.oci.security import Vault
from diagrams.oci.database import Autonomous
from diagrams.oci.storage import ObjectStorage
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.client import User

with Diagram("Jenkins on OCI Deployment Architecture", show=False, direction="TB"):
    user = User("User")
    internet = InternetGateway("Internet Gateway")
    lb = LoadBalancer("Load Balancer")
    vcn = Vcn("VCN")
    route_table = RouteTable("Route Table")
    security_lists = SecurityLists("Security Lists")
    key_vault = Vault("Key Vault")
    jenkins_controller = Jenkins("Jenkins Controller")
    jenkins_agent = Jenkins("Jenkins Agent")
    database = Autonomous("Database")
    storage = ObjectStorage("Object Storage")

    user >> internet >> lb
    lb >> vcn
    vcn >> route_table
    vcn >> security_lists
    vcn >> key_vault
    vcn >> jenkins_controller
    vcn >> jenkins_agent
    jenkins_controller >> database
    jenkins_controller >> storage
    jenkins_agent >> jenkins_controller