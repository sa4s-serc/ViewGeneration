from diagrams import Diagram, Cluster, Edge
from diagrams.programming.framework import React
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.database import MongoDB
from diagrams.onprem.network import Nginx
from diagrams.aws.security import Cognito 
from diagrams.aws.integration import SNS
from diagrams.aws.compute import Lambda

with Diagram("TIBC Architecture", show=False, direction="TB"):
    
    with Cluster("Core Protocol"):
        client_semantics = Lambda("Client Semantics")
        port_packet = Lambda("Port & Packet")
        host_env = Lambda("Host Environments") 
        packet_routing = Lambda("Packet Routing")
        
        core_components = [client_semantics, port_packet, host_env, packet_routing]

    with Cluster("Client Implementations"):
        tendermint = Lambda("Tendermint Client")
        bsc = Lambda("BSC Client")
        ethereum = Lambda("Ethereum Client")
        
        clients = [tendermint, bsc, ethereum]

    with Cluster("Applications"):
        nft = Lambda("NFT Transfer")
        routing = SNS("Routing Module")
        
        apps = [nft, routing]

    with Cluster("Relayer Layer"):
        queue = RabbitMQ("Message Queue")
        storage = MongoDB("State Storage")
        gateway = Nginx("API Gateway")
        
        relayer_components = [queue, storage, gateway]

    # Connect components
    for core in core_components:
        for client in clients:
            core >> Edge() >> client
            
    for client in clients:
        for relay in relayer_components:
            client >> Edge() >> relay
            
    for relay in relayer_components:
        for app in apps:
            relay >> Edge() >> app