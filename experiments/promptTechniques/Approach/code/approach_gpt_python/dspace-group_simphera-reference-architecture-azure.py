from diagrams import Diagram
from diagrams.azure.compute import ACR, AKS
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.security import KeyVaults
from diagrams.azure.network import VirtualNetworks, PrivateEndpoint, Subnets
from diagrams.azure.storage import ArchiveStorage

with Diagram("SIMPHERA Azure Reference Architecture", show=False):
    vnet = VirtualNetworks("Virtual Network")
    subnets = Subnets("Subnets")
    vnet >> subnets

    aks = AKS("Kubernetes Cluster")
    db = DatabaseForPostgresqlServers("PostgreSQL Flexible Servers")
    minio = ArchiveStorage("MinIO Storage Accounts")
    keyvault = KeyVaults("Azure Key Vault")
    private_link = PrivateEndpoint("Private Link")

    aks - db
    aks - minio
    aks - keyvault
    aks - private_link

    subnets >> aks
    subnets >> db
    subnets >> minio
    subnets >> keyvault
    subnets >> private_link