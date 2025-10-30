from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import ACR, AKS, VM, AppServices
from diagrams.azure.identity import ActiveDirectory, ADB2C, ADDomainServices
from diagrams.azure.database import CosmosDb
from diagrams.azure.devops import ApplicationInsights
from diagrams.aws.migration import ADS
from diagrams.azure.network import LoadBalancers
from diagrams.azure.monitor import Monitor

with Diagram("SpektraSystems_CloudLabs-Azure Architecture", show=False):
    with Cluster("Azure Migrate"):
        on_prem = ADS("On-premises Hyper-V VMs")
        migrate = ACR("Azure Migrate")
        migrate >> on_prem

    with Cluster("Azure Virtual Machines & Compute"):
        vm_cluster = [VM("VM1"), VM("VM2"), VM("VM3")]
        lb = LoadBalancers("Load Balancer")
        lb >> vm_cluster

    with Cluster("Serverless App Modernization"):
        with Cluster("Microservices"):
            function1 = AppServices("Azure Function 1")
            function2 = AppServices("Azure Function 2")
            function3 = AppServices("Azure Function 3")
            functions = [function1, function2, function3]
            functions >> CosmosDb("Cosmos DB")

        blazor_app = AppServices("Blazor Web App")
        blazor_app >> functions

    with Cluster("Azure Monitoring"):
        monitor = Monitor("Azure Monitor")
        insights = ApplicationInsights("App Insights")
        monitor >> insights

    with Cluster("Identity and Access Management"):
        ad = ActiveDirectory("Azure Active Directory")
        adb2c = ADB2C("Azure AD B2C")
        domain_services = ADDomainServices("AD Domain Services")
        ad >> Edge(label="authenticates") >> adb2c
        ad >> Edge(label="integrates with") >> domain_services