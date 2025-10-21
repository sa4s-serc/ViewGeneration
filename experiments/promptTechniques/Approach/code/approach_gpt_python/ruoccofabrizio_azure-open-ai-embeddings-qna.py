from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import FunctionApps
from diagrams.azure.storage import BlobStorage
from diagrams.azure.web import AppServices
from diagrams.azure.database import CosmosDb
from diagrams.onprem.client import Client
from diagrams.onprem.vcs import Github
from diagrams.generic.database import SQL
from diagrams.programming.framework import React
from diagrams.programming.language import Python
from diagrams.azure.integration import ServiceBusQueues

with Diagram("Azure OpenAI Embeddings QnA Architecture", show=False, direction="TB"):
    user = Client("User")
    
    with Cluster("Web Application Layer"):
        web_app = AppServices("Streamlit Web App")
        user >> web_app

    with Cluster("Batch Processing"):
        batch_start = FunctionApps("BatchStartProcessing")
        batch_push = FunctionApps("BatchPushResults")
        
        web_app >> Edge(label="HTTP Trigger") >> batch_start
        batch_start >> Edge(label="Queue Message") >> ServiceBusQueues("Azure Queue")
        ServiceBusQueues("Azure Queue") >> Edge(label="Trigger") >> batch_push

    with Cluster("Storage and Embeddings"):
        blob_storage = BlobStorage("Blob Storage")
        vector_store = SQL("Vector Store (Redis/PGVector)")
        
        batch_push >> Edge(label="Read/Write") >> blob_storage
        batch_push >> Edge(label="Embedding Creation") >> vector_store

    with Cluster("Vector Search Options"):
        azure_search = CosmosDb("Azure Cognitive Search")
        
        web_app >> Edge(label="Query Vector Store") >> vector_store
        vector_store >> Edge(label="Semantic Search") >> azure_search

    with Cluster("Azure OpenAI Service"):
        azure_openai = Python("Azure OpenAI")
        vector_store >> Edge(label="Embedding Creation") >> azure_openai
        azure_openai >> Edge(label="Answer Generation") >> web_app

    with Cluster("Development and Deployment"):
        github = Github("GitHub Repo")
        docker = React("Docker")
        
        github >> Edge(label="CI/CD") >> docker
        docker >> Edge(label="Deploy") >> [web_app, batch_start, batch_push]