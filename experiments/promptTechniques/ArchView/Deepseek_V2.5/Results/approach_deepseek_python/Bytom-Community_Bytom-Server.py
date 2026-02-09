from diagrams import Diagram, Cluster
from diagrams.onprem.network import Apache
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow

with Diagram("Bytom Server Architecture", show=False):
    with Cluster("Client Layer"):
        client = Server("Client")
    
    with Cluster("API Gateway"):
        api_gateway = Apache("gRPC API")
    
    with Cluster("Application Layer"):
        with Cluster("Core Blockchain"):
            protocol = Server("Protocol")
            tx_pool = Server("TxPool")
            validation = Server("Validation")
        
        with Cluster("Networking"):
            p2p = Server("P2P")
            netsync = Server("NetSync")
        
        with Cluster("Transaction Processing"):
            tx_builder = Server("Tx Builder")
            vm = Server("BVM")
            state_mgmt = Server("State Management")
        
        with Cluster("Mining"):
            mining = Server("CPU Mining")
            tensority = Server("Tensority")
    
    with Cluster("Data Layer"):
        with Cluster("Storage"):
            db = PostgreSQL("LevelDB")
            utxo_index = Server("UTXO Index")
        
        with Cluster("Caching"):
            cache = Redis("Cache")
        
        with Cluster("Messaging"):
            queue = Kafka("Event Queue")
    
    with Cluster("Security Layer"):
        auth = Server("Access Token")
        pseudohsm = Server("Pseudohsm")
        key_mgmt = Server("Key Management")
    
    with Cluster("Monitoring"):
        monitoring = Grafana("Monitoring")
        logging = Server("Logging")
    
    with Cluster("Orchestration"):
        orchestration = Airflow("Workflow")
        container = Docker("Container Runtime")
    
    client >> api_gateway
    api_gateway >> [protocol, tx_pool, validation, p2p, netsync, tx_builder, vm, state_mgmt, mining, tensority]
    protocol >> [tx_pool, validation, p2p, netsync]
    tx_pool >> tx_builder
    tx_builder >> vm
    vm >> state_mgmt
    state_mgmt >> db
    p2p >> netsync
    netsync >> db
    mining >> tensority
    tensority >> protocol
    [protocol, tx_pool, validation, p2p, netsync, tx_builder, vm, state_mgmt, mining, tensority] >> cache
    [protocol, tx_pool, validation, p2p, netsync, tx_builder, vm, state_mgmt, mining, tensority] >> queue
    api_gateway >> auth
    auth >> pseudohsm
    pseudohsm >> key_mgmt
    [protocol, tx_pool, validation, p2p, netsync, tx_builder, vm, state_mgmt, mining, tensority] >> monitoring
    [protocol, tx_pool, validation, p2p, netsync, tx_builder, vm, state_mgmt, mining, tensority] >> logging
    orchestration >> container
    container >> [protocol, tx_pool, validation, p2p, netsync, tx_builder, vm, state_mgmt, mining, tensority]