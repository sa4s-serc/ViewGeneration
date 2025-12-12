from diagrams import Diagram, Cluster
from diagrams.azure.compute import AppServices
from diagrams.azure.database import CosmosDb
from diagrams.azure.storage import BlobStorage
from diagrams.azure.identity import ADB2C
from diagrams.azure.integration import APIManagement
from diagrams.azure.ml import CognitiveServices
from diagrams.azure.security import KeyVaults

with Diagram("UnoCash Architecture", show=False):
    with Cluster("Frontend"):
        blazor = AppServices("UnoCash.Blazor")

    with Cluster("Backend Services"):
        api = APIManagement("UnoCash.Api")
        auth = ADB2C("Authentication")
        key_vault = KeyVaults("Secrets")

        with Cluster("Core Services"):
            receipt = CognitiveServices("Receipt Parser")
            expenses = CosmosDb("Expense Storage")
            storage = BlobStorage("Receipt Storage")

    # Frontend connections
    blazor >> api

    # Backend connections
    api >> auth
    api >> key_vault
    api >> receipt
    api >> expenses
    api >> storage

    # Receipt processing flow
    storage >> receipt
    receipt >> expenses