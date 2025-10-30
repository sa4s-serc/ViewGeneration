from diagrams import Diagram
from diagrams.ibm.applications import ActionableInsight
from diagrams.ibm.applications import Annotate
from diagrams.ibm.applications import Index
from diagrams.ibm.applications import Microservice
from diagrams.onprem.database import MongoDB
from diagrams.ibm.general import IBMPublicCloud
from diagrams.onprem.client import User
from diagrams.onprem.network import Internet

with Diagram("Serverless Chatbot Architecture", show=False):
    user = User("User")
    internet = Internet("Internet")
    ibm_cloud = IBMPublicCloud("IBM Cloud")

    user >> internet >> ibm_cloud

    ibm_cloud_actionable_insight = ActionableInsight("IBM Cloud Functions")
    ibm_cloud_annotate = Annotate("Watson Assistant")
    ibm_cloud_index = Index("MongoDB (Optional)")
    ibm_cloud_microservice = Microservice("FaaS Architecture")

    ibm_cloud >> ibm_cloud_actionable_insight
    ibm_cloud >> ibm_cloud_annotate
    ibm_cloud >> ibm_cloud_index
    ibm_cloud >> ibm_cloud_microservice

    ibm_cloud_actionable_insight >> ibm_cloud_annotate
    ibm_cloud_annotate >> ibm_cloud_index