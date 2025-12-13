from diagrams import Diagram, Cluster
from diagrams.azure.network import Firewall, ApplicationGateway
from diagrams.azure.web import AppServices
from diagrams.azure.database import SQLDatabases
from diagrams.azure.security import KeyVaults
from diagrams.azure.general import Resourcegroups

with Diagram("Secure PaaS Deployment on Azure", direction="TB", filename="secure_paas_azure_architecture", show=False):
    with Cluster("Azure Environment"):
        app_service = AppServices("Azure App Service")
        sql_db = SQLDatabases("Azure SQL Database")
        waf = ApplicationGateway("Web Application Firewall (WAF)")
        firewall = Firewall("Azure Firewall")
        key_vault = KeyVaults("Azure Key Vault")
        resource_group = Resourcegroups("Resource Group")

    app_service >> waf >> firewall >> sql_db
    app_service >> firewall
    app_service >> key_vault

    resource_group - [app_service, sql_db, waf, firewall, key_vault]