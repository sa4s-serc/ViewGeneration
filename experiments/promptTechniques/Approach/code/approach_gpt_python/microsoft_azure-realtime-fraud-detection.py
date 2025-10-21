from diagrams import Diagram
from diagrams.azure.analytics import StreamAnalyticsJobs
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import CosmosDb, SynapseAnalytics
from diagrams.azure.machinelearning import Workspaces
from diagrams.azure.integration import EventHubs
from diagrams.custom import Custom

with Diagram("Fraud Detection Platform on Azure", show=False, direction="LR"):
    event_generator = Custom("Event Generator", "./icons/event_generator.png")
    event_hub = EventHubs("Azure Event Hub")
    
    event_generator >> event_hub
    
    stream_analytics = StreamAnalyticsJobs("Azure Stream Analytics")
    event_hub >> stream_analytics
    
    synapse = SynapseAnalytics("Azure Synapse Analytics")
    cosmos_sql = CosmosDb("Azure Cosmos DB\n(SQL API)")
    cosmos_gremlin = CosmosDb("Azure Cosmos DB\n(Gremlin API)")
    
    stream_analytics >> synapse
    stream_analytics >> cosmos_sql
    stream_analytics >> cosmos_gremlin
    
    ml = Workspaces("Azure Machine Learning")
    stream_analytics >> ml
    
    functions = FunctionApps("Azure Functions")
    ml >> functions
    functions >> cosmos_gremlin
    
    functions << Custom("Benford's Law Calculation", "./icons/benfords_law.png")
    functions << Custom("Fraud Ring Identification", "./icons/fraud_ring.png")