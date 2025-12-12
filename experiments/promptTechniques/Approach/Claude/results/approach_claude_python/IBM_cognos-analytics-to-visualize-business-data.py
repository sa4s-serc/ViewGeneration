from diagrams import Diagram, Cluster
from diagrams.aws.database import RDS
from diagrams.aws.compute import EC2
from diagrams.ibm.analytics import DataIntegration 
from diagrams.azure.analytics import DataFactories
from diagrams.firebase.develop import Authentication
from diagrams.aws.storage import S3
from diagrams.ibm.applications import ApiDeveloperPortal

with Diagram("IBM Cognos Analytics Architecture", show=False):
    auth = Authentication("Authentication")
    
    with Cluster("Data Sources"):
        db2 = RDS("DB2 Warehouse")
        netezza = EC2("Netezza Server")
        data_files = S3("Business Data Files")
    
    with Cluster("Data Integration Layer"):
        etl = DataIntegration("ETL Processing")
        data_factory = DataFactories("Data Factory")
    
    with Cluster("Analytics Layer"):
        cognos = ApiDeveloperPortal("Cognos Analytics")
    
    # Data flow
    data_files >> etl
    db2 >> etl
    netezza >> etl
    
    etl >> data_factory
    data_factory >> cognos
    
    auth >> cognos