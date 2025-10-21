from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.ibm.cloud import Functions as IBMCloudFunctions
from diagrams.ibm.analytics import WatsonAssistant
from diagrams.onprem.database import Mongodb

with Diagram("Serverless Chatbot Architecture", show=False):
    user = Custom("User", "./user.png")  # Custom icon for User

    with Cluster("IBM Cloud Functions"):
        assistant_function = IBMCloudFunctions("assistant.js")
        mongodb_function = IBMCloudFunctions("mongodb.js")

    assistant = WatsonAssistant("Watson Assistant")
    mongodb = Mongodb("MongoDB")

    user >> assistant_function
    assistant_function >> assistant
    assistant_function >> mongodb_function
    mongodb_function >> mongodb