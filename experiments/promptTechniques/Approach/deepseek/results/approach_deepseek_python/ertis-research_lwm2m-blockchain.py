from diagrams import Diagram, Cluster
from diagrams.aws.general import User
from diagrams.aws.mobile import APIGateway
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.onprem.client import User as OnPremUser
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import Spring, Angular
from diagrams.generic.database import SQL
from diagrams.generic.network import Firewall
from diagrams.generic.storage import Storage
from diagrams.generic.device import Mobile
from diagrams.custom import Custom

with Diagram("LwM2M and Blockchain System Architecture", show=False, direction="TB"):
    user = User("End User")
    iot_device = Mobile("IoT Device")

    with Cluster("Frontend Layer"):
        anomaly_app = Angular("Anomaly Detection App")
        management_app = Angular("Management App")

    with Cluster("API Gateway"):
        api_gateway = APIGateway("REST API Gateway")

    with Cluster("Backend Services"):
        with Cluster("Spring Boot Backend"):
            client_controller = Spring("Client Controller")
            anomaly_controller = Spring("Anomaly Controller")
            user_controller = Spring("User Controller")
            login_controller = Spring("Login Controller")
        
        with Cluster("Business Logic"):
            client_service = Spring("Client Service")
            anomaly_service = Spring("Anomaly Service")
            user_service = Spring("User Service")
            blockchain_service = Spring("Blockchain Service")

    with Cluster("LwM2M Components"):
        with Cluster("LwM2M Server"):
            lwm2m_server = EC2("LwM2M Server")
            leshan_library = Custom("Eclipse Leshan", "./leshan_icon.png")
        
        with Cluster("Bootstrap Server"):
            bootstrap_server = EC2("Bootstrap Server")
            security_store = Custom("Security Store", "./security_icon.png")
        
        with Cluster("LwM2M Client"):
            lwm2m_client = EC2("LwM2M Client")
            device_objects = Custom("Device Objects", "./device_icon.png")

    with Cluster("Blockchain Layer"):
        with Cluster("Smart Contracts"):
            user_store = Custom("UserStore.sol", "./contract_icon.png")
            client_store = Custom("ClientStore.sol", "./contract_icon.png")
            anomaly_store = Custom("AnomalyStore.sol", "./contract_icon.png")
        
        with Cluster("Blockchain Network"):
            ethereum = Custom("Ethereum", "./ethereum_icon.png")
            web3j = Custom("Web3j Wrapper", "./web3j_icon.png")

    with Cluster("Data Storage"):
        with Cluster("On-chain Storage"):
            blockchain_storage = Storage("Blockchain Storage")
        
        with Cluster("Off-chain Storage"):
            local_db = PostgreSQL("Local Database")
            cache_db = Redis("Cache")

    with Cluster("Security"):
        jwt_auth = Cognito("JWT Authentication")
        access_control = Firewall("Access Control")

    user >> anomaly_app >> api_gateway
    user >> management_app >> api_gateway
    iot_device >> lwm2m_server
    lwm2m_server >> api_gateway
    bootstrap_server >> lwm2m_client
    lwm2m_client >> lwm2m_server
    
    api_gateway >> jwt_auth
    api_gateway >> client_controller >> client_service
    api_gateway >> anomaly_controller >> anomaly_service
    api_gateway >> user_controller >> user_service
    api_gateway >> login_controller >> jwt_auth
    
    client_service >> blockchain_service >> web3j >> ethereum
    anomaly_service >> blockchain_service >> web3j >> ethereum
    user_service >> blockchain_service >> web3j >> ethereum
    
    web3j >> user_store
    web3j >> client_store
    web3j >> anomaly_store
    
    user_store >> blockchain_storage
    client_store >> blockchain_storage
    anomaly_store >> blockchain_storage
    
    client_service >> local_db
    anomaly_service >> local_db
    user_service >> local_db
    
    client_service >> cache_db
    anomaly_service >> cache_db
    
    bootstrap_server >> security_store >> web3j >> client_store