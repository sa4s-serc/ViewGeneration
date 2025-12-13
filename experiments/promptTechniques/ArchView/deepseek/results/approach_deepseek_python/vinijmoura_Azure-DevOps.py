from diagrams import Diagram
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import SQLDatabases
from diagrams.azure.devops import Pipelines
from diagrams.azure.analytics import DataFactories
from diagrams.azure.integration import LogicApps
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.security import KeyVaults
from diagrams.azure.monitor import Monitor
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.web import AppServices

with Diagram("Azure DevOps Power BI Reporting Architecture", show=False, direction="LR"):
    with Diagram("Data Extraction Layer"):
        ad_identity = ActiveDirectory("Azure AD")
        key_vault = KeyVaults("Key Vault")
        devops_pipelines = Pipelines("Azure DevOps")
        logic_apps = LogicApps("Logic Apps")
        function_apps = FunctionApps("Function Apps")
        
        ad_identity >> key_vault
        key_vault >> devops_pipelines
        key_vault >> logic_apps
        key_vault >> function_apps

    with Diagram("Data Processing Layer"):
        data_factory = DataFactories("Data Factory")
        storage_account = StorageAccounts("Blob Storage")
        sql_database = SQLDatabases("SQL Database")
        
        devops_pipelines >> data_factory
        logic_apps >> data_factory
        function_apps >> data_factory
        data_factory >> storage_account
        data_factory >> sql_database

    with Diagram("Presentation Layer"):
        app_gateway = ApplicationGateway("App Gateway")
        app_services = AppServices("App Service")
        power_bi = AppServices("Power BI")
        monitor = Monitor("Azure Monitor")
        
        app_gateway >> app_services
        app_services >> power_bi
        sql_database >> power_bi
        monitor << [devops_pipelines, data_factory, sql_database, app_services]