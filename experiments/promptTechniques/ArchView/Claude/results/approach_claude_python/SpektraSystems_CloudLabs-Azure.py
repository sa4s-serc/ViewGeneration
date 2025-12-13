from diagrams import Diagram, Cluster
from diagrams.azure.compute import AppServices, ContainerRegistries, KubernetesServices
from diagrams.azure.database import CosmosDb
from diagrams.azure.storage import BlobStorage
from diagrams.azure.devops import Artifacts, ApplicationInsights
from diagrams.azure.integration import APIManagement
from diagrams.azure.identity import ActiveDirectory

with Diagram("CloudLabs Azure Architecture", show=False):
    with Cluster("Azure Cloud"):
        # Identity and Access
        ad = ActiveDirectory("Azure AD")
        
        # API Layer
        api = APIManagement("API Gateway")
        
        with Cluster("Compute Services"):
            # Container and Kubernetes
            acr = ContainerRegistries("Container Registry")
            aks = KubernetesServices("AKS")
            apps = AppServices("App Services")
        
        # Data Layer
        with Cluster("Data Services"):
            cosmos = CosmosDb("Cosmos DB")
            blob = BlobStorage("Blob Storage")
        
        # DevOps and Monitoring
        artifacts = Artifacts("Azure Artifacts")
        insights = ApplicationInsights("App Insights")
        
        # Define relationships
        ad >> api
        api >> [aks, apps]
        acr >> aks
        aks >> cosmos
        apps >> [cosmos, blob]
        [aks, apps] >> insights
        artifacts >> [aks, apps]