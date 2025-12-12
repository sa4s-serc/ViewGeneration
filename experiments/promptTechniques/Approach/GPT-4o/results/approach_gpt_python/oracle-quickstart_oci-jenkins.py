from diagrams import Diagram, Cluster
from diagrams.onprem.ci import Jenkins
from diagrams.oci.database import ADB
from diagrams.oci.network import Vcn, LoadBalancerWhite, SecurityLists
from diagrams.oci.compute import BM
from diagrams.oci.connectivity import NATGatewayWhite

with Diagram("Jenkins on OCI Deployment with Terraform", show=False):
    with Cluster("OCI Infrastructure"):
        vcn = Vcn("Virtual Cloud Network")
        nat_gateway = NATGatewayWhite("NAT Gateway")
        security_list = SecurityLists("Security List")
        lb = LoadBalancerWhite("Load Balancer")

        with Cluster("Jenkins Cluster"):
            controller = Jenkins("Jenkins Controller")
            agents = [Jenkins("Agent 1"),
                      Jenkins("Agent 2"),
                      Jenkins("Agent 3")]

        db = ADB("Autonomous Database")

    vcn >> nat_gateway >> lb >> controller >> agents
    vcn >> security_list >> db
    nat_gateway >> vcn