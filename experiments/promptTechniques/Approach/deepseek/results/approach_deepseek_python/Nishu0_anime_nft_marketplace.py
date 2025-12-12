from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import React, Nextjs
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mongodb
from diagrams.generic.storage import Storage
from diagrams.onprem.network import Internet
from diagrams.generic.compute import Rack
from diagrams.generic.device import Mobile

with Diagram("Anime NFT Marketplace Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Frontend Layer"):
        frontend = Nextjs("Next.js App")
        react = React("React Components")
        frontend >> react
    
    with Cluster("Context Layer"):
        context = Server("NFT Context")
    
    with Cluster("Blockchain Layer"):
        blockchain = Rack("Ethereum/Polygon")
        smart_contract = Server("NFTMarketplace.sol")
        blockchain >> smart_contract
    
    with Cluster("Storage Layer"):
        ipfs = Storage("IPFS Storage")
        metadata_db = Mongodb("Metadata DB")
    
    with Cluster("External Services"):
        metamask = Mobile("Metamask Wallet")
        internet = Internet("Web3 Provider")
    
    user >> frontend
    frontend >> context
    context >> smart_contract
    context >> ipfs
    context >> metadata_db
    user >> metamask
    metamask >> internet
    internet >> blockchain
    smart_contract >> ipfs