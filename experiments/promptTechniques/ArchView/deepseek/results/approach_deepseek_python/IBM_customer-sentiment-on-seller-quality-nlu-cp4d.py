from diagrams import Diagram
from diagrams.aws.database import RDS
from diagrams.aws.ml import Comprehend
from diagrams.ibm.analytics import DataIntegration
from diagrams.ibm.management import AlertNotification
from diagrams.programming.language import Python

with Diagram("Seller Quality Analysis Architecture", show=False, direction="LR"):
    db2 = RDS("Db2 Database")
    
    notebook = Python("Jupyter Notebook\n(customer-sentiment-on-seller.ipynb)")
    
    watson_nlu = Comprehend("Watson NLU")
    
    dashboard = AlertNotification("Embedded Dashboard")
    
    db2 >> notebook
    notebook >> watson_nlu
    notebook >> dashboard