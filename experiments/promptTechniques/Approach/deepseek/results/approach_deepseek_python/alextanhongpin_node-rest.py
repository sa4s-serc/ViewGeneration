from diagrams import Diagram
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import MySQL
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.tracing import Jaeger
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Nodejs
from diagrams.onprem.compute import Server

with Diagram("Food Service Application Architecture", show=False, direction="TB"):
    client = Server("Client")
    
    with Diagram("Application Layer"):
        api_gateway = Nginx("API Gateway")
        food_service = Nodejs("Food Service")
        
        with Diagram("Business Layer"):
            food_model = Nodejs("Food Model")
            validation = Nodejs("Validation")
            
        with Diagram("Data Layer"):
            food_store = Nodejs("Food Store")
            database = MySQL("MySQL Database")
    
    with Diagram("Infrastructure Layer"):
        docker = Docker("Docker")
        config = Nodejs("Config Management")
        tests = Nodejs("Unit Tests")
    
    client >> api_gateway
    api_gateway >> food_service
    food_service >> food_model
    food_model >> validation
    food_model >> food_store
    food_store >> database
    
    docker - [api_gateway, food_service, food_model, food_store, database]
    config - [api_gateway, food_service, food_model, food_store]
    tests - [food_model, food_store]