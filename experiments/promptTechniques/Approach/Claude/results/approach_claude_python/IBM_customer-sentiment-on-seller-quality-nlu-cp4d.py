from diagrams import Diagram, Cluster
from diagrams.aws.database import RDS
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import Comprehend
from diagrams.aws.storage import S3
from diagrams.ibm.analytics import DataIntegration
from diagrams.azure.analytics import Databricks
from diagrams.gcp.analytics import BigQuery
from diagrams.onprem.analytics import Tableau

with Diagram("Seller Quality Analysis Architecture", show=False):
    with Cluster("Data Sources"):
        db = RDS("DB2 Database")
        reviews = S3("Customer Reviews")

    with Cluster("Processing Layer"):
        notebook = DataIntegration("Jupyter Notebook")
        nlu = Comprehend("Watson NLU")
        
    with Cluster("Analysis Layer"):
        sentiment = Lambda("Sentiment Analysis")
        delivery = Lambda("Delivery Analysis")
        
    with Cluster("Data Storage"):
        analytics_store = BigQuery("Analytics Data")
        
    with Cluster("Visualization"):
        dashboard = Tableau("Quality Dashboard")

    db >> notebook
    reviews >> notebook
    notebook >> nlu
    nlu >> sentiment
    db >> delivery
    sentiment >> analytics_store
    delivery >> analytics_store
    analytics_store >> dashboard