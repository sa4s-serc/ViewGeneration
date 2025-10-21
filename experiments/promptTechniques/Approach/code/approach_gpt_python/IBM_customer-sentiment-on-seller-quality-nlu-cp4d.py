from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.ibm.analytics import Nlu
from diagrams.onprem.monitoring import Grafana
from diagrams.ibm.storage import Db2

with Diagram("Seller Quality Analysis Architecture", direction="LR"):

    db2 = Db2("Db2 Database")
    watson_nlu = Nlu("Watson NLU")
    jupyter = Custom("Jupyter Notebook", "https://jupyter.org/assets/homepage/main-logo.svg")
    dashboard = Grafana("Embedded Dashboard")

    with Cluster("Data Processing Pipeline"):
        jupyter >> Edge(label="data extraction") >> db2
        db2 >> Edge(label="data transformation") >> jupyter
        jupyter >> Edge(label="sentiment analysis") >> watson_nlu
        watson_nlu >> Edge(label="sentiment scores") >> jupyter
        jupyter >> Edge(label="quality ratings") >> dashboard

    dashboard << Edge(label="interactive visualization") << jupyter