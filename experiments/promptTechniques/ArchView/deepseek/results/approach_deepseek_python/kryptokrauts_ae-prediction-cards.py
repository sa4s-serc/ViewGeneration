from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import React
from diagrams.aws.blockchain import BlockchainResource
from diagrams.aws.general import GenericDatabase

with Diagram("kryptokrauts_ae-prediction-cards Architecture", show=False, direction="TB"):
    users = User("Users")
    
    frontend = React("Frontend\n(React)")
    
    wallet_client = Server("Wallet Client\n(Superhero)")
    prediction_api = Server("Prediction API\n(aepp-sdk-js)")
    
    blockchain = BlockchainResource("Aeternity Blockchain")
    smart_contract = Server("Smart Contract\n(PredictionCards.aes)")
    
    oracle_service = Server("Oracle Service\n(Java)")
    process_service = Server("Process Prediction Service\n(Java)")
    
    backend_db = PostgreSQL("Backend Database")
    cache = Redis("Cache")
    
    users >> frontend
    frontend >> wallet_client
    frontend >> prediction_api
    wallet_client >> blockchain
    prediction_api >> blockchain
    blockchain >> smart_contract
    
    oracle_service >> blockchain
    process_service >> blockchain
    process_service >> oracle_service
    
    oracle_service >> backend_db
    process_service >> backend_db
    frontend >> backend_db
    frontend >> cache