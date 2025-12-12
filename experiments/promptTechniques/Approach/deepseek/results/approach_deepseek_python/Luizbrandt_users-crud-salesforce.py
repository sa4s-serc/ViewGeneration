from diagrams import Diagram, Cluster
from diagrams.aws.general import Client, Users
from diagrams.aws.network import APIGateway
from diagrams.aws.integration import StepFunctions
from diagrams.aws.database import Dynamodb
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch

with Diagram("Salesforce User CRUD System API", show=False, direction="LR"):
    client = Client("Client Application")
    
    with Cluster("MuleSoft API Layer"):
        api_gateway = APIGateway("API Kit Router")
        
        with Cluster("Mule Flows"):
            create_flow = StepFunctions("Create Flow")
            read_flow = StepFunctions("Read Flow")
            update_flow = StepFunctions("Update Flow")
            delete_flow = StepFunctions("Delete Flow")
        
        dataweave = StepFunctions("DataWeave\nTransformations")
        error_handling = StepFunctions("Error Handling")
    
    salesforce = Users("Salesforce\nCustom_User__c Object")
    
    with Cluster("Configuration Layer"):
        secure_props = IAM("Secure Properties")
        global_config = Cloudwatch("Global Config")
        raml_spec = Dynamodb("RAML Specification")
    
    client >> api_gateway
    
    api_gateway >> create_flow
    api_gateway >> read_flow
    api_gateway >> update_flow
    api_gateway >> delete_flow
    
    create_flow >> dataweave
    read_flow >> dataweave
    update_flow >> dataweave
    delete_flow >> dataweave
    
    create_flow >> error_handling
    read_flow >> error_handling
    update_flow >> error_handling
    delete_flow >> error_handling
    
    dataweave >> salesforce
    
    secure_props >> dataweave
    global_config >> dataweave
    raml_spec >> api_gateway