from diagrams import Diagram
from diagrams.onprem.database import Dgraph, InfluxDB
from diagrams.onprem.queue import EMQX
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.workflow import Airflow
from diagrams.programming.framework import React, GraphQL
from diagrams.generic.device import Tablet
from diagrams.generic.network import Switch
from diagrams.custom import Custom

with Diagram("Libre Core/Platform Architecture", show=False, direction="TB"):
    # External clients
    user = Tablet("User")
    edge_agent = Custom("Edge Agent", "./resources/edge_agent.png")
    
    # Core platform components
    admin_ui = React("Libre Administration UI")
    gateway = GraphQL("GraphQL Gateway")
    
    # Microservices
    core_service = Custom("Libre Core", "./resources/microservice.png")
    pubsub_service = Custom("GraphQL PubSub", "./resources/microservice.png")
    workflow_engine = Airflow("Workflow Engine")
    
    # Data layer
    dgraph = Dgraph("Dgraph")
    influxdb = InfluxDB("InfluxDB")
    
    # Communication layer
    mqtt_broker = EMQX("MQTT Broker")
    
    # Visualization layer
    grafana = Grafana("Grafana Dashboards")
    
    # Connections
    user >> admin_ui
    edge_agent >> mqtt_broker
    
    admin_ui >> gateway
    gateway >> [core_service, pubsub_service, workflow_engine]
    
    core_service >> dgraph
    pubsub_service >> mqtt_broker
    workflow_engine >> dgraph
    
    mqtt_broker >> influxdb
    influxdb >> grafana
    
    # Internal service communication
    core_service >> pubsub_service
    pubsub_service >> workflow_engine