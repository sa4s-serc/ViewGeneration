from diagrams import Diagram, Cluster
from diagrams.azure.analytics import EventHubs
from diagrams.azure.compute import FunctionApps
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.database import CosmosDb
from diagrams.azure.analytics import SynapseAnalytics
from diagrams.azure.integration import EventGridTopics
from diagrams.azure.storage import DataLakeStorage

with Diagram("Fraud Detection Platform Architecture", show=False):
    with Cluster("Data Ingestion"):
        eventhub = EventHubs("Event Hub")
        eventgrid = EventGridTopics("Event Grid")

    with Cluster("Processing & ML"):
        functions = FunctionApps("Azure Functions")
        ml = MachineLearningServiceWorkspaces("Machine Learning")

    with Cluster("Storage & Analytics"):
        cosmos = CosmosDb("Cosmos DB")
        synapse = SynapseAnalytics("Synapse Analytics")
        datalake = DataLakeStorage("Data Lake")

    # Data flow
    eventhub >> functions
    functions >> ml
    ml >> cosmos
    functions >> eventgrid
    eventgrid >> datalake
    datalake >> synapse
    cosmos >> synapse