from diagrams import Diagram, Cluster
from diagrams.azure.network import VirtualNetworks, Subnets
from diagrams.azure.compute import AKS, VM
from diagrams.azure.database import PostgreSQLServers
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.security import KeyVaults
from diagrams.azure.analytics import LogAnalyticsWorkspaces
from diagrams.azure.general import Resourcegroups

with Diagram("SIMPHERA Azure Reference Architecture", show=False):
    with Cluster("Azure Infrastructure"):
        vnet = VirtualNetworks("Virtual Network")
        
        with Cluster("Subnets"):
            aks_subnet = Subnets("AKS Subnet")
            pgsql_subnet = Subnets("PostgreSQL Subnet")
            paas_subnet = Subnets("PaaS Services Subnet")
            bastion_subnet = Subnets("Bastion Host Subnet")
            license_subnet = Subnets("License Server Subnet")

        aks = AKS("Kubernetes Cluster")
        postgres = PostgreSQLServers("PostgreSQL Flexible Servers")
        storage = StorageAccounts("MinIO Storage Accounts")
        keyvault = KeyVaults("Azure Key Vault")
        log_analytics = LogAnalyticsWorkspaces("Log Analytics")

        with Cluster("Optional Components"):
            license_server = VM("License Server")
            bastion_host = VM("Bastion Host")

        vnet >> aks_subnet >> aks
        vnet >> pgsql_subnet >> postgres
        vnet >> paas_subnet >> storage
        vnet >> paas_subnet >> keyvault
        vnet >> paas_subnet >> log_analytics
        vnet >> license_subnet >> license_server
        vnet >> bastion_subnet >> bastion_host

    rg = Resourcegroups("Resource Group")
    rg >> vnet
    rg >> [aks, postgres, storage, keyvault, log_analytics, license_server, bastion_host]