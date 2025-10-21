from diagrams import Cluster, Diagram, Edge
from diagrams.azure.devops import Devops
from diagrams.azure.database import SQLDatabases
from diagrams.azure.analytics import DataLake
from diagrams.onprem.client import User
from diagrams.programming.language import Powershell

with Diagram("Azure DevOps Power BI Reporting Architecture", show=False, direction="LR"):
    user = User("User")
    
    with Cluster("Azure DevOps"):
        devops = Devops("Azure DevOps")
        extraction_scripts = [
            Powershell("User Access"),
            Powershell("Project Management"),
            Powershell("Code Repositories"),
            Powershell("Build & Release Pipelines"),
            Powershell("Team Configuration"),
            Powershell("Packaging"),
            Powershell("Environments & Approvals"),
            Powershell("Task Groups"),
            Powershell("Service Hooks"),
            Powershell("Extensions")
        ]
        
    with Cluster("Data Transformation"):
        transformation_scripts = [Powershell("Transform Data")]

    with Cluster("Data Storage"):
        sql_db = SQLDatabases("Azure SQL Database")
        
    with Cluster("Data Visualization"):
        power_bi = DataLake("Power BI")
    
    user >> Edge(label="Access via CLI/API") >> devops
    devops >> Edge(label="Execute Scripts") >> extraction_scripts
    extraction_scripts >> Edge(label="Transform Data") >> transformation_scripts
    transformation_scripts >> Edge(label="Load Data") >> sql_db
    sql_db >> Edge(label="Visualize Data") >> power_bi
    user << Edge(label="View Reports") << power_bi