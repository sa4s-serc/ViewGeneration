from diagrams import Diagram, Cluster
from diagrams.onprem.network import Apache
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import PostgreSQL

with Diagram("TIBC Architecture", show=False, direction="TB"):
    with Cluster("TIBC Core Protocol"):
        client_semantics = Server("Client Semantics\n(TICS-002)")
        port_packet = Server("Port & Packet Semantics\n(TICS-004)")
        host_env = Server("Host Environments\n(TICS-024)")
        packet_routing = Server("Packet Routing\n(TICS-026)")
    
    with Cluster("Client Implementations"):
        tendermint = Server("Tendermint Client\n(TICS-007)")
        bsc = Server("BSC Client\n(TICS-008)")
        ethereum = Server("Ethereum Client\n(TICS-009)")
    
    with Cluster("Applications"):
        nft_transfer = Server("NFT Transfer\n(TICS-030)")
    
    with Cluster("Infrastructure"):
        relayer = Server("Relayer Algorithms")
        routing_module = Server("Routing Module")
    
    client_semantics >> [tendermint, bsc, ethereum]
    port_packet >> nft_transfer
    packet_routing >> routing_module
    routing_module >> relayer
    [tendermint, bsc, ethereum] >> relayer
    relayer >> [client_semantics, port_packet, host_env]