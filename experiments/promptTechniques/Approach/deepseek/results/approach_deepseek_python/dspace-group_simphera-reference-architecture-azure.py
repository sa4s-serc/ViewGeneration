from diagrams import Diagram
from diagrams.azure.compute import AKS, VM
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.security import KeyVaults
from diagrams.azure.network import VirtualNetworks, PrivateEndpoint
from diagrams.azure.general import Usericon
from diagrams.azure.devops import Pipelines
from diagrams.onprem.vcs import Git
from diagrams.onprem.iac import Terraform

with Diagram("SIMPHERA Azure Reference Architecture", show=False, direction="TB"):
    user = Usericon("User")
    
    with Diagram("Infrastructure as Code"):
        git = Git("Git Repository")
        terraform = Terraform("Terraform")
        pipelines = Pipelines("GitHub Actions")
        git >> terraform
        git >> pipelines
    
    with Diagram("Azure Infrastructure"):
        vnet = VirtualNetworks("Virtual Network")
        
        with Diagram("Compute"):
            aks = AKS("AKS Cluster")
            license_vm = VM("License Server VM")
            aks >> license_vm
        
        with Diagram("Database"):
            postgres_keycloak = DatabaseForPostgresqlServers("PostgreSQL Keycloak")
            postgres_simphera = DatabaseForPostgresqlServers("PostgreSQL SIMPHERA")
            private_link_db = PrivateEndpoint("Private Link")
            postgres_keycloak >> private_link_db
            postgres_simphera >> private_link_db
        
        with Diagram("Storage"):
            minio = StorageAccounts("MinIO Storage")
            private_link_storage = PrivateEndpoint("Private Link")
            minio >> private_link_storage
        
        with Diagram("Security"):
            key_vault = KeyVaults("Azure Key Vault")
        
        vnet - [aks, license_vm, private_link_db, private_link_storage, key_vault]
    
    user >> aks
    aks >> [postgres_keycloak, postgres_simphera, minio, key_vault]
    terraform >> [aks, postgres_keycloak, postgres_simphera, minio, key_vault, vnet]