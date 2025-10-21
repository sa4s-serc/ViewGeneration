from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.client import User
from diagrams.programming.language import Nodejs
from diagrams.ibm.analytics import CognosAnalytics

with Diagram("Data Visualization with IBM Cognos Analytics", show=False, direction="LR"):

    client = User("User")

    with Cluster("Data Generation"):
        nodejs = Nodejs("Node.js")
        data_files = Custom("CSV Files", "./csv-icon.png")
        nodejs >> Edge(label="generates") >> data_files

    with Cluster("Data Warehouse"):
        db2 = PostgreSQL("IBM Db2 Warehouse")
        netezza = PostgreSQL("Netezza Performance Server")
        data_files >> Edge(label="loads into") >> db2
        data_files >> Edge(label="loads into") >> netezza

    with Cluster("Cognos Analytics"):
        cognos = CognosAnalytics("IBM Cognos Analytics")
        cognos << Edge(label="connects to") << db2
        cognos << Edge(label="connects to") << netezza
        cognos << Edge(label="creates dashboards") << client

    nodejs >> Edge(label="runs scripts") >> cognos