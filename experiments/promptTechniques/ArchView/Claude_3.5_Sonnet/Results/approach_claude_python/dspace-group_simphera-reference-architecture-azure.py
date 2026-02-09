from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import AKS
from diagrams.azure.database import CosmosDb
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.network import Subnets, VirtualNetworks, PrivateEndpoint
from diagrams.azure.compute import ContainerInstances
from diagrams.azure.identity import ActiveDirectory

with Diagram("SIMPHERA Azure Reference Architecture", show=False):
    with Cluster("Virtual Network"):
        network = VirtualNetworks("VNET")
        
        with Cluster("Network Subnets"):
            aks_subnet = Subnets("AKS Subnet")
            db_subnet = Subnets("DB Subnet")
            storage_subnet = Subnets("Storage Subnet")
            
    # Core Services
    aks = AKS("Kubernetes\nCluster")
    keycloak_db = CosmosDb("Keycloak DB")
    simphera_db = CosmosDb("SIMPHERA DB")
    key_vault = KeyVaults("Key Vault")
    minio = StorageAccounts("MinIO Storage")
    aad = ActiveDirectory("Azure AD")
    
    # Private Endpoints
    db_pe = PrivateEndpoint("DB Private\nEndpoint")
    storage_pe = PrivateEndpoint("Storage Private\nEndpoint")
    
    # Connections
    network >> aks_subnet >> aks
    network >> db_subnet >> db_pe
    network >> storage_subnet >> storage_pe
    
    db_pe >> keycloak_db
    db_pe >> simphera_db
    storage_pe >> minio
    
    aks >> key_vault
    aks >> aad
    
    # Optional Components
    with Cluster("Optional Components"):
        bastion = ContainerInstances("Bastion Host")
        license_server = ContainerInstances("License Server")
        
        network >> bastion
        network >> license_server