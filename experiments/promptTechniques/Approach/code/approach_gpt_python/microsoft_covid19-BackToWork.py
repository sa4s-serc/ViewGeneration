from diagrams import Diagram, Cluster
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import SQLDatabases
from diagrams.azure.devops import Pipelines
from diagrams.generic.compute import Rack
from diagrams.onprem.client import Users
from diagrams.onprem.notification import Email

with Diagram("Back to Work Solution Architecture", show=False):
    users = Users("Employees")
    
    with Cluster("Azure Functions"):
        http_post_funcs = [
            FunctionApps("PostUserInfo"),
            FunctionApps("PostSymptomsInfo"),
            FunctionApps("PostLabTestInfo"),
            FunctionApps("PostRequestStatus"),
        ]
        
        http_get_funcs = [
            FunctionApps("GetUserInfo"),
            FunctionApps("GetSymptomsInfo"),
            FunctionApps("GetLabTestInfo"),
            FunctionApps("GetRequestStatus"),
        ]
        
        notification_func = FunctionApps("TriggerNotification")
    
    sql_db = SQLDatabases("Azure SQL Database")
    healthcare_bot = Rack("Microsoft Healthcare Bot")
    arm_templates = Pipelines("ARM Templates")
    
    users >> http_post_funcs >> sql_db
    users >> http_get_funcs << sql_db
    healthcare_bot >> http_get_funcs
    notification_func >> Email("SendGrid Email") >> users
    notification_func >> Rack("Microsoft Teams")
    arm_templates >> FunctionApps("Automated Deployment")