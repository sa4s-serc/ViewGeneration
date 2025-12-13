from diagrams import Diagram, Cluster
from diagrams.azure.compute import AppServices
from diagrams.azure.database import SQLDatabases
from diagrams.azure.network import ApplicationGateway, Firewall
from diagrams.azure.security import KeyVaults
from diagrams.azure.network import PrivateEndpoint
from diagrams.azure.network import VirtualNetworks

with Diagram("Secure PaaS Deployment Architecture", show=False, direction="LR"):
    
    with Cluster("Azure Virtual Network"):
        vnet = VirtualNetworks("VNet")
        
        with Cluster("Application Gateway Subnet"):
            waf = ApplicationGateway("WAF")

        with Cluster("App Service Subnet"):
            app = AppServices("App Service")
            
        with Cluster("Azure Firewall Subnet"):
            firewall = Firewall("Azure Firewall")
            
        with Cluster("Database Subnet"):
            db = SQLDatabases("Azure SQL")
            db_ep = PrivateEndpoint("Private Endpoint")
            
    secrets = KeyVaults("Key Vault")

    # Define the flow
    waf >> app
    app >> firewall
    firewall >> db_ep >> db
    app >> secrets