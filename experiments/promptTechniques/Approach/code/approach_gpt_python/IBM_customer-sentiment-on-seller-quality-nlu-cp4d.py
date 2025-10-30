from diagrams import Diagram
from diagrams.ibm.applications import ApiDeveloperPortal, AppServer, ActionableInsight
from diagrams.ibm.analytics import DataIntegration
from diagrams.ibm.data import DataServices
from diagrams.ibm.infrastructure import MobileBackend
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Envoy

with Diagram("Seller Quality Analysis Using Watson NLU", show=False):
    postgres = PostgreSQL("Db2 Database")
    nlu = ApiDeveloperPortal("Watson NLU")
    notebook = AppServer("Jupyter Notebook")
    dashboard = ActionableInsight("Embedded Dashboard Service")

    postgres >> notebook >> nlu
    nlu >> DataIntegration("Sentiment Analysis") >> DataServices("Data Processing Pipeline")
    notebook >> DataIntegration("Seller Rating Calculation") >> DataServices("Visualization Dataset")
    docker = Docker("Cloud Pak for Data or IBM Cloud")
    notebook >> docker >> MobileBackend("Deployment Environment")
    dashboard << Envoy("Interactive Visualization") << notebook