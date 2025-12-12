from diagrams import Diagram, Cluster
from diagrams.azure.analytics import EventHubs, StreamAnalyticsJobs, SynapseAnalytics
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import CosmosDb
from diagrams.custom import Custom

with Diagram("Fraud Detection Platform Architecture", show=False, direction="LR"):
    event_generator = Custom("Event Generator", "./custom_icons/event_generator.png")

    with Cluster("Azure Services"):
        event_hub = EventHubs("Event Hub")
        
        with Cluster("Stream Processing"):
            stream_analytics = StreamAnalyticsJobs("Stream Analytics")
            
        with Cluster("Machine Learning"):
            ml_workspace = MachineLearningServiceWorkspaces("ML Workspace")
            
        with Cluster("Function Orchestration"):
            functions = FunctionApps("Azure Functions")
            
        with Cluster("Data Storage"):
            synapse = SynapseAnalytics("Synapse Analytics")
            cosmos_sql = CosmosDb("Cosmos DB (SQL API)")
            cosmos_gremlin = CosmosDb("Cosmos DB (Gremlin API)")

    event_generator >> event_hub
    event_hub >> stream_analytics
    stream_analytics >> ml_workspace
    stream_analytics >> synapse
    stream_analytics >> cosmos_sql
    stream_analytics >> cosmos_gremlin
    ml_workspace >> functions
    functions >> cosmos_gremlin