from diagrams import Diagram, Cluster, Edge
from diagrams.oci.compute import Instance
from diagrams.oci.network import VCN, Subnet, InternetGateway, NATGateway, LoadBalancer
from diagrams.oci.security import Bastion
from diagrams.oci.identity import Identity

with Diagram("Jenkins on OCI Deployment with Terraform", show=False, direction="TB"):
    user = Identity("Jenkins Admin")

    with Cluster("OCI Cloud"):
        vcn = VCN("Virtual Cloud Network")
        igw = InternetGateway("Internet Gateway")
        nat_gw = NATGateway("NAT Gateway")

        with Cluster("Subnets"):
            controller_subnet = Subnet("Controller Subnet")
            agent_subnet = Subnet("Agent Subnet")
            bastion_subnet = Subnet("Bastion Subnet")
            lb_subnet = Subnet("Load Balancer Subnet")

        with Cluster("Jenkins Cluster"):
            controller = Instance("Jenkins Controller")
            agents = [Instance("Jenkins Agent 1"),
                      Instance("Jenkins Agent 2")]

        lb = LoadBalancer("OCI Load Balancer")
        bastion = Bastion("Bastion Service")

    user >> Edge(label="SSH Access") >> bastion
    bastion >> Edge(label="Secure Connection") >> controller
    igw >> Edge(label="Public Network Access") >> vcn
    nat_gw >> Edge(label="Outbound Access") >> vcn
    vcn >> Edge(label="Network Flow") >> controller_subnet >> controller
    vcn >> agent_subnet >> agents
    vcn >> bastion_subnet >> bastion
    vcn >> lb_subnet >> lb
    lb >> Edge(label="Traffic Distribution") >> controller
    controller >> Edge(label="Job Execution") >> agents