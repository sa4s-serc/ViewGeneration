from diagrams import Diagram
from diagrams.ibm.applications import ActionableInsight
from diagrams.ibm.data import DataSources
from diagrams.ibm.infrastructure import MobileBackend
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx

with Diagram("IBM Cognos Analytics Architecture", show=False):
    data_sources = DataSources("Business Data")
    db = PostgreSQL("Db2 Warehouse")
    netezza = PostgreSQL("Netezza Performance Server")
    cognos = ActionableInsight("IBM Cognos Analytics")
    nodejs = Nginx("Node.js")
    mobile_backend = MobileBackend("Mobile Backend")

    data_sources >> db
    data_sources >> netezza
    db >> cognos
    netezza >> cognos
    cognos >> mobile_backend
    nodejs >> data_sources
    nodejs >> db
    nodejs >> netezza