from diagrams import Cluster, Diagram, Edge
from diagrams.azure.devops import Pipelines, Artifacts, Repos
from diagrams.azure.database import SQLDatabases
from diagrams.azure.identity import ActiveDirectory 
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server

with Diagram("Azure DevOps Power BI Reporting Architecture", show=False):
    with Cluster("Azure DevOps"):
        repos = Repos("Azure DevOps\nRepositories")
        ad = ActiveDirectory("Azure AD\nAuthentication")
        artifacts = Artifacts("Azure DevOps\nArtifacts")
        pipelines = Pipelines("Azure DevOps\nPipelines")

    with Cluster("ETL Process"):
        ps = Server("PowerShell\nScripts")
        db = SQLDatabases("Azure SQL\nDatabase")

    with Cluster("Reporting"):
        powerbi = Users("Power BI\nReports")

    # Data flow
    repos >> ps
    ad >> ps
    artifacts >> ps
    pipelines >> ps
    ps >> db
    db >> powerbi