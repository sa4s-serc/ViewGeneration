from diagrams import Diagram, Cluster
from diagrams.azure.ml import AzureOpenAI
from diagrams.azure.compute import ACR, AKS
from diagrams.azure.web import AppServices
from diagrams.azure.storage import BlobStorage
from diagrams.onprem.queue import Activemq
from diagrams.onprem.vcs import Github
from diagrams.programming.language import Python
from diagrams.azure.devops import Pipelines

with Diagram("Azure OpenAI Embeddings QnA Architecture", show=False):
    developer = Github("Developer")

    with Cluster("Azure Services"):
        openai_service = AzureOpenAI("OpenAI Service")
        aks = AKS("Azure Kubernetes Service")
        acr = ACR("Azure Container Registry")
        app_service = AppServices("App Service")
        blob_storage = BlobStorage("Blob Storage")

    with Cluster("Question Answering System"):
        question_answering = Python("QnA System")
        embeddings = AzureOpenAI("Embeddings Creation")
        batch_processing = Activemq("Batch Processing")

    developer >> Pipelines("CI/CD Pipeline") >> acr

    acr >> aks >> app_service >> question_answering

    question_answering >> openai_service
    question_answering >> embeddings >> batch_processing >> blob_storage

    question_answering << developer