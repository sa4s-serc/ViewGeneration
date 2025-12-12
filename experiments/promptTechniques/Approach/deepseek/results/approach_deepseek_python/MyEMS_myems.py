from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Angular
from diagrams.onprem.database import MySQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.inmemory import Redis

with Diagram("MyEMS Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        admin_ui = Angular("Admin UI")
        web_ui = Angular("Web UI")
    
    with Cluster("API Layer"):
        api_gateway = Nginx("API Gateway")
        falcon_api = Server("Falcon API")
    
    with Cluster("Services Layer"):
        with Cluster("Data Processing"):
            modbus_service = Server("Modbus TCP Service")
            cleaning_service = Server("Data Cleaning")
            normalization = Server("Normalization")
            aggregation = Server("Aggregation")
        
        with Cluster("Business Services"):
            user_mgmt = Server("User Management")
            reporting = Server("Reporting")
            billing = Server("Billing")
            fdd = Server("FDD")
    
    with Cluster("Data Layer"):
        with Cluster("MySQL Databases"):
            system_db = MySQL("System DB")
            energy_db = MySQL("Energy DB")
            billing_db = MySQL("Billing DB")
            historical_db = MySQL("Historical DB")
            carbon_db = MySQL("Carbon DB")
        
        cache = Redis("Cache")
        message_queue = Kafka("Message Queue")
    
    with Cluster("Monitoring"):
        monitoring = Grafana("Monitoring")
    
    user >> admin_ui
    user >> web_ui
    admin_ui >> api_gateway
    web_ui >> api_gateway
    api_gateway >> falcon_api
    
    falcon_api >> user_mgmt
    falcon_api >> reporting
    falcon_api >> billing
    falcon_api >> fdd
    
    modbus_service >> message_queue
    message_queue >> cleaning_service
    cleaning_service >> normalization
    normalization >> aggregation
    aggregation >> energy_db
    
    user_mgmt >> system_db
    reporting >> [energy_db, historical_db, carbon_db]
    billing >> billing_db
    fdd >> system_db
    
    falcon_api >> cache
    cache >> [system_db, energy_db, billing_db, historical_db, carbon_db]
    
    [modbus_service, cleaning_service, normalization, aggregation, 
     user_mgmt, reporting, billing, fdd] >> monitoring