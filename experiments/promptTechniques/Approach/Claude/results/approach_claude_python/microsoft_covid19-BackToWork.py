from diagrams import Diagram, Cluster
from diagrams.azure.compute import AppServices
from diagrams.azure.database import SQLDatabases 
from diagrams.azure.integration import APIManagement
from diagrams.azure.security import KeyVaults
from diagrams.azure.integration import LogicApps
from diagrams.azure.integration import EventGridDomains
from diagrams.azure.integration import ServiceBus
from diagrams.azure.web import AppServicePlans

with Diagram("Back to Work Solution Architecture", show=False):
    with Cluster("Azure Cloud"):
        api = APIManagement("API Gateway")
        
        with Cluster("Core Services"):
            bot = AppServicePlans("Healthcare Bot")
            app = AppServices("Azure Functions")
            db = SQLDatabases("Azure SQL DB")
            vault = KeyVaults("Key Vault")
        
        with Cluster("Integration Layer"):
            logic = LogicApps("Logic Apps")
            events = EventGridDomains("Event Grid")
            bus = ServiceBus("Service Bus")

        # Core flow
        api >> app
        app >> db
        app >> vault
        
        # Bot integration
        bot >> api
        
        # Event handling
        app >> events
        events >> logic
        logic >> bus
        bus >> app

        # Data flow
        app >> db