from diagrams import Diagram
from diagrams.azure.analytics import EventHubs, StreamAnalyticsJobs, SynapseAnalytics
from diagrams.azure.database import CosmosDb
from diagrams.azure.compute import FunctionApps
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.integration import LogicApps

with Diagram("Fraud Detection Platform on Azure", show=False, direction="TB"):
    event_hub = EventHubs("Azure Event Hub")
    stream_analytics = StreamAnalyticsJobs("Azure Stream Analytics")
    machine_learning = MachineLearningServiceWorkspaces("Azure Machine Learning")
    azure_functions = FunctionApps("Azure Functions")
    synapse_analytics = SynapseAnalytics("Azure Synapse Analytics")
    cosmos_db = CosmosDb("Azure Cosmos DB")
    event_generator = LogicApps("Event Generator")

    event_generator >> event_hub
    event_hub >> stream_analytics
    stream_analytics >> synapse_analytics
    stream_analytics >> cosmos_db
    stream_analytics >> machine_learning
    machine_learning >> azure_functions
    azure_functions >> cosmos_db
    azure_functions >> event_hub