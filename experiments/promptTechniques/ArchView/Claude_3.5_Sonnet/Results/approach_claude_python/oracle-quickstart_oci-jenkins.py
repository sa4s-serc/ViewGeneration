from diagrams import Diagram
from diagrams.oci.compute import Container, BareMetalWhite, VMWhite
from diagrams.oci.network import LoadBalancerWhite, VcnWhite
from diagrams.oci.security import Vault, CloudGuard
from diagrams.oci.connectivity import CustomerPremises, BackboneWhite
from diagrams.oci.database import DatabaseService
from diagrams.oci.governance import Compartments

with Diagram("Jenkins on OCI Deployment Architecture", show=False):
    
    # Network components
    vcn = VcnWhite("Virtual Cloud Network")
    lb = LoadBalancerWhite("Load Balancer")
    bastion = CustomerPremises("Bastion Host")
    backbone = BackboneWhite("OCI Network")

    # Security components
    vault = Vault("Security Vault")
    security = CloudGuard("Security Rules")

    # Compute components
    jenkins_controller = Container("Jenkins Controller")
    jenkins_agents = [Container("Jenkins Agent") for _ in range(2)]
    
    # Database and storage
    db = DatabaseService("Database")
    
    # Organization
    compartment = Compartments("Resource Compartment")

    # Network flow
    backbone >> vcn
    vcn >> lb
    lb >> jenkins_controller
    bastion >> jenkins_controller
    jenkins_controller >> jenkins_agents
    
    # Security associations
    vault >> jenkins_controller
    security >> vcn
    
    # Resource organization
    compartment >> [vcn, jenkins_controller, db]
    
    # Database connections
    jenkins_controller >> db