from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.queue import Kafka
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.programming.framework import Spring
from diagrams.generic.blank import Blank

with Diagram("Auditor-v1 Architecture", show=False, direction="TB"):
    with Cluster("Client Applications"):
        spring_app = Spring("Spring Boot App")
        standalone_app = Spring("Standalone App")
        client_library = Blank("Client Library")
        
        spring_app >> client_library
        standalone_app >> client_library
    
    with Cluster("Application Server"):
        with Cluster("/app"):
            main_app = Blank("Application.kt")
            consumer_service = Blank("ConsumerService.kt")
            repository_service = Blank("AuditEventRepositoryService.kt")
            
            main_app >> consumer_service
            consumer_service >> repository_service
    
    with Cluster("Core Module"):
        core_components = [
            Blank("AuditEventDTOMapper.kt"),
            Blank("AuditEventMapper.kt"), 
            Blank("JsonObject.kt")
        ]
    
    with Cluster("Infrastructure"):
        kafka = Kafka("Kafka")
        elasticsearch = Elasticsearch("Elasticsearch")
    
    # Data flow connections
    client_library >> kafka
    kafka >> consumer_service
    repository_service >> elasticsearch
    
    # Core module usage
    client_library - core_components
    consumer_service - core_components
    repository_service - core_components