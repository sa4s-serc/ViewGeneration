from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

with Diagram("TIBC Architecture", show=False, direction="TB"):
    client = Custom("Light Clients", "./client.png")

    with Cluster("TIBC Core Protocol"):
        core_protocol = Custom("Core Protocol", "./protocol.png")
        client_semantics = Custom("Client Semantics", "./client_semantics.png")
        port_packet_semantics = Custom("Port & Packet Semantics", "./port_packet_semantics.png")
        host_environments = Custom("Host Environments", "./host_environments.png")
        packet_routing = Custom("Packet Routing", "./packet_routing.png")

        core_protocol - client_semantics
        core_protocol - port_packet_semantics
        core_protocol - host_environments
        core_protocol - packet_routing

    with Cluster("Client Implementations"):
        tendermint_client = Custom("Tendermint Client", "./tendermint.png")
        bsc_client = Custom("BSC Client", "./bsc.png")
        ethereum_client = Custom("Ethereum Client", "./ethereum.png")

        client - tendermint_client
        client - bsc_client
        client - ethereum_client

    with Cluster("Relayer Algorithms"):
        relayer_algorithms = Custom("Relayer Algorithms", "./relayer_algorithms.png")
        relayer_algorithms - Edge(label="scans & executes", style="dashed") - core_protocol

    nft_transfer_app = Custom("NFT Transfer Application", "./nft_transfer.png")
    routing_module = Custom("Routing Module", "./routing_module.png")

    nft_transfer_app - Edge(label="utilizes", style="dotted") - routing_module
    routing_module - Edge(label="routes packets", style="dotted") - relayer_algorithms

    core_protocol >> Edge(label="interacts with") >> nft_transfer_app
    client >> Edge(label="verifies state") >> core_protocol