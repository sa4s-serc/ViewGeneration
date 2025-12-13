from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import Lex
from diagrams.onprem.database import Mongodb
from diagrams.aws.integration import StepFunctions

with Diagram("Serverless Chatbot Architecture", show=False, direction="LR"):
    user = Lambda("User Input")
    ibm_cloud_functions = Lambda("IBM Cloud Functions")
    watson_assistant = Lex("Watson Assistant")
    mongodb = Mongodb("MongoDB")
    
    user >> ibm_cloud_functions
    ibm_cloud_functions >> watson_assistant
    watson_assistant >> ibm_cloud_functions
    ibm_cloud_functions >> mongodb