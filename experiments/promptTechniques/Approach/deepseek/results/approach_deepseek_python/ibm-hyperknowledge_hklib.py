from diagrams import Diagram
from diagrams.generic.blank import Blank
from diagrams.programming.language import Javascript, Typescript
from diagrams.onprem.client import Client
from diagrams.onprem.database import Cassandra
from diagrams.onprem.network import Apache
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.compute import Server

with Diagram("hklib Architecture", show=False, direction="TB"):
    client = Client("Browser/NodeJS Client")
    
    with Diagram("Core Entity Layer"):
        hk_entity = Blank("HKEntity (Abstract)")
        node = Blank("Node")
        context = Blank("Context")
        link = Blank("Link")
        connector = Blank("Connector")
        reference = Blank("Reference")
        trail = Blank("Trail")
        virtual_node = Blank("VirtualNode")
        virtual_context = Blank("VirtualContext")
        virtual_link = Blank("VirtualLink")
        
        hk_entity >> [node, context, link, connector, reference, trail]
        node >> virtual_node
        context >> virtual_context
        link >> virtual_link
    
    with Diagram("Data Access Layer"):
        hk_datasource = Blank("HKDatasource")
        hk_graph = Blank("HKGraph")
        deserialize = Blank("Deserialize")
        hyperify = Blank("Hyperify")
        
        hk_datasource >> hk_graph
        deserialize >> hk_graph
        hyperify >> hk_graph
    
    with Diagram("Observer Pattern"):
        observer_factory = Blank("HKObserverFactory")
        observer_client = Blank("ObserverClient")
        rest_observer = Blank("REST Observer")
        rabbitmq_observer = Rabbitmq("RabbitMQ Observer")
        
        observer_factory >> observer_client
        observer_client >> [rest_observer, rabbitmq_observer]
    
    with Diagram("Fragment Identifiers"):
        fi = Blank("FI")
        fi_anchor = Blank("FIAnchor")
        fi_operator = Blank("FIOperator")
        
        fi >> [fi_anchor, fi_operator]
    
    with Diagram("External Integration"):
        wordnet = Blank("Wordnet")
        dbpedia = Blank("DBpedia")
        external_sources = [wordnet, dbpedia]
    
    with Diagram("Utility Layer"):
        graph_builder = Blank("Graph Builder")
        stored_queries = Blank("Stored Queries")
        authentication = Blank("Authentication")
        types = Blank("Types")
        
        utility_components = [graph_builder, stored_queries, authentication, types]
    
    client >> hk_datasource
    client >> observer_factory
    hk_datasource >> [hk_entity, hk_graph]
    hk_datasource >> external_sources
    hk_datasource >> utility_components
    observer_client >> hk_datasource
    fi >> hk_entity