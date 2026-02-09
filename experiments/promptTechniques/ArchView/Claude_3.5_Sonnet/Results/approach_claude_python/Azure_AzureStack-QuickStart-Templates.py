from diagrams import Cluster, Diagram, Edge
from diagrams.azure.compute import AppServices, ContainerInstances, AKS
from diagrams.azure.database import SQLDatabases, CosmosDb
from diagrams.azure.storage import BlobStorage
from diagrams.azure.network import LoadBalancers
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.security import KeyVaults
from diagrams.azure.devops import Pipelines

with Diagram("Azure Stack QuickStart Templates Architecture", show=False):
    with Cluster("Security & Identity"):
        ad = ActiveDirectory("Azure AD")
        kv = KeyVaults("Key Vault")
    
    with Cluster("Deployment"):
        pipe = Pipelines("Azure Pipelines")
        
    with Cluster("Compute Services"):
        lb = LoadBalancers("Load Balancer")
        with Cluster("Container Platform"):
            aks = AKS("AKS")
            ci = ContainerInstances("Container Instances")
        apps = AppServices("App Services")

    with Cluster("Data Services"):
        sql = SQLDatabases("SQL Database")
        cosmos = CosmosDb("Cosmos DB")
        blob = BlobStorage("Blob Storage")

    # Core deployment flow
    pipe >> Edge(color="darkgreen") >> [aks, ci, apps]
    
    # Security dependencies
    ad >> Edge(color="red") >> [aks, apps]
    kv >> Edge(color="red") >> [aks, apps, sql]
    
    # Network flow
    lb >> Edge(color="blue") >> [aks, ci, apps]
    
    # Data access
    apps >> Edge(color="orange") >> [sql, cosmos, blob]
    aks >> Edge(color="orange") >> [sql, cosmos, blob]