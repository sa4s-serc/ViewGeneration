from diagrams import Diagram, Cluster
from diagrams.azure.ml import AzureOpenAI
from diagrams.azure.database import CosmosDb
from diagrams.azure.compute import ContainerInstances
from diagrams.azure.web import AppServices
from diagrams.azure.storage import BlobStorage
from diagrams.azure.integration import ServiceBus
from diagrams.azure.compute import FunctionApps

with Diagram("Azure OpenAI Embeddings QnA Architecture", show=False):
    with Cluster("Web Application"):
        webapp = AppServices("Streamlit Web App")

    with Cluster("Vector Stores"):
        stores = [
            CosmosDb("Azure Cognitive Search"),
            BlobStorage("Redis"),
            CosmosDb("PGVector")
        ]

    with Cluster("Azure OpenAI Services"):
        openai = [
            AzureOpenAI("Embeddings Generation"),
            AzureOpenAI("GPT Answer Generation")
        ]

    with Cluster("Batch Processing"):
        queue = ServiceBus("Azure Queue")
        func1 = FunctionApps("Start Processing")
        func2 = FunctionApps("Push Results")
        storage = BlobStorage("Blob Storage")

        func1 >> queue >> func2
        storage << func2

    webapp >> openai
    webapp >> stores
    func2 >> stores[0]
    openai[0] >> stores