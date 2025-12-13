from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.network import ELB, VPC, PrivateSubnet, PublicSubnet, InternetGateway, NATGateway
from diagrams.aws.database import Dynamodb
from diagrams.aws.management import Cloudformation
from diagrams.aws.integration import SNS

with Diagram("MarkLogic Cloud Enablement on AWS", show=False, direction="TB"):
    with Cluster("VPC"):
        igw = InternetGateway("Internet Gateway")
        nat = NATGateway("NAT Gateway")
        public_subnet = PublicSubnet("Public Subnet")
        private_subnet = PrivateSubnet("Private Subnet")
        
        with Cluster("Auto Scaling Group"):
            instance1 = EC2("MarkLogic Node 1")
            instance2 = EC2("MarkLogic Node 2")
            instanceN = EC2("MarkLogic Node n")
        
        elb = ELB("Application Load Balancer")
        
        public_subnet - igw
        private_subnet - nat
        elb >> Edge(label="distributes traffic") >> [instance1, instance2, instanceN]

    cf_stack = Cloudformation("CloudFormation Stack")
    ddb_table = Dynamodb("MarkLogicDDBTable")
    sns = SNS("Event Logging (Optional)")

    cf_stack >> Edge(label="provisions") >> [instance1, instance2, instanceN, elb, ddb_table]
    
    with Cluster("Lambda Functions"):
        managed_eni = Lambda("managedeni.py")
        node_manager = Lambda("nodemanager.py")
        utils = Lambda("utils.py")
        
    cf_stack >> Edge(label="custom logic") >> [managed_eni, node_manager]
    managed_eni >> Edge(label="ENI management") >> [instance1, instance2, instanceN]
    node_manager >> Edge(label="instance lifecycle") >> [instance1, instance2, instanceN]

    [instance1, instance2, instanceN] >> Edge(label="state management") >> ddb_table
    cf_stack >> Edge(label="logging") >> sns