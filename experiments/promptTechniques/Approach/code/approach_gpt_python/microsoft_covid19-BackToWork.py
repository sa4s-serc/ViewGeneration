from diagrams import Diagram
from diagrams.azure.compute import ACR, FunctionApps
from diagrams.azure.database import SQLDatabases
from diagrams.saas.cdn import Cloudflare
from diagrams.azure.integration import APIForFhir, ServiceBus
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.web import APIConnections
from diagrams.firebase.grow import DynamicLinks
from diagrams.oci.monitoring import Email
from diagrams.firebase.develop import Functions

with Diagram("Back to Work Solution Architecture", show=False):
    user = DynamicLinks("User")
    
    auth = ActiveDirectory("Azure AD")
    bot = APIForFhir("Healthcare Bot")
    functions = FunctionApps("Azure Functions")
    db = SQLDatabases("Azure SQL Database")
    notifications = Email("SendGrid Email")
    teams = ServiceBus("Microsoft Teams")
    api = APIConnections("API Management")
    
    user >> auth >> bot
    bot >> functions
    functions >> db
    functions >> notifications
    functions >> teams
    functions >> api