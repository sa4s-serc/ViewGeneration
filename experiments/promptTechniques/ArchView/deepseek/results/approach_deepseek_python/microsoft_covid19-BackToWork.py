from diagrams import Diagram, Cluster
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import SQLDatabases
from diagrams.azure.web import AppServices
from diagrams.azure.integration import LogicApps
from diagrams.azure.security import KeyVaults
from diagrams.generic.network import Firewall
from diagrams.onprem.client import Users
from diagrams.generic.device import Mobile
from diagrams.azure.identity import ActiveDirectory

with Diagram("Back to Work Solution Architecture", show=False, direction="TB"):
    users = Users("Employees")
    mobile_users = Mobile("Mobile Users")
    
    with Cluster("Azure Cloud"):
        with Cluster("Presentation Layer"):
            healthcare_bot = AppServices("Healthcare Bot")
            web_chat = AppServices("Web Chat Channel")
        
        with Cluster("Application Layer"):
            with Cluster("Azure Functions"):
                post_user = FunctionApps("PostUserInfo")
                post_symptoms = FunctionApps("PostSymptomsInfo")
                post_lab = FunctionApps("PostLabTestInfo")
                post_status = FunctionApps("PostRequestStatus")
                get_user = FunctionApps("GetUserInfo")
                get_symptoms = FunctionApps("GetSymptomsInfo")
                get_lab = FunctionApps("GetLabTestInfo")
                get_status = FunctionApps("GetRequestStatus")
                trigger_notification = FunctionApps("TriggerNotification")
            
            logic_apps = LogicApps("Notification Logic")
        
        with Cluster("Data Layer"):
            sql_db = SQLDatabases("Azure SQL Database")
        
        with Cluster("Security & Identity"):
            key_vault = KeyVaults("Key Vault")
            ad = ActiveDirectory("Azure AD")
            firewall = Firewall("Network Security")
    
    with Cluster("External Services"):
        sendgrid = AppServices("SendGrid")
        teams = AppServices("Microsoft Teams")
        powerbi = AppServices("Power BI")
    
    # User interactions
    users >> healthcare_bot
    mobile_users >> web_chat
    web_chat >> healthcare_bot
    
    # Bot to Functions communication
    healthcare_bot >> [post_user, post_symptoms, post_lab, post_status]
    healthcare_bot << [get_user, get_symptoms, get_lab, get_status]
    
    # Data flow between functions and database
    [post_user, post_symptoms, post_lab, post_status] >> sql_db
    [get_user, get_symptoms, get_lab, get_status] << sql_db
    
    # Notification flow
    trigger_notification >> logic_apps
    logic_apps >> [sendgrid, teams]
    
    # Reporting and analytics
    sql_db >> powerbi
    
    # Security and configuration
    [post_user, post_symptoms, post_lab, post_status, 
     get_user, get_symptoms, get_lab, get_status, 
     trigger_notification, healthcare_bot] << key_vault
    
    # Identity management
    [users, mobile_users] >> ad
    [healthcare_bot, web_chat] << ad
    
    # Network security
    users >> firewall >> healthcare_bot
    mobile_users >> firewall >> web_chat