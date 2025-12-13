from diagrams import Diagram
from diagrams.azure.web import AppServices
from diagrams.azure.database import SQLDatabases
from diagrams.azure.network import Firewall, ApplicationGateway
from diagrams.azure.security import KeyVaults
from diagrams.azure.network import PrivateEndpoint

with Diagram("Secure PaaS Deployment on Azure", show=False, direction="TB"):
    with Diagram("Hub Network"):
        firewall = Firewall("Azure Firewall")
        waf = ApplicationGateway("WAF")
    
    with Diagram("Spoke Network"):
        app_service = AppServices("App Service")
        sql_db = SQLDatabases("SQL Database")
        key_vault = KeyVaults("Key Vault")
        private_endpoint = PrivateEndpoint("Private Endpoint")
        
        waf >> app_service
        app_service >> firewall
        firewall >> private_endpoint
        private_endpoint >> sql_db
        app_service >> key_vault