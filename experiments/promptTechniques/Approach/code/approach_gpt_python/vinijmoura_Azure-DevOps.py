from diagrams import Diagram, Cluster
from diagrams.azure.devops import Pipelines, Repos, Boards, Artifacts
from diagrams.onprem.analytics import PowerBI
from diagrams.onprem.iac import Ansible
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.container import Docker
from diagrams.azure.database import SQLDatabases

with Diagram("Azure DevOps Power BI Reporting Architecture", show=False):
    devops = Pipelines("Azure DevOps")

    with Cluster("ETL Pipeline"):
        extract = Ansible("Data Extraction")
        transform = Ansible("Data Transformation")
        load = Ansible("Data Load")

    data_storage = SQLDatabases("Azure SQL Database")
    visualization = PowerBI("Power BI")

    devops >> extract >> transform >> load >> data_storage
    data_storage >> visualization