from diagrams import Diagram, Cluster
from diagrams.onprem.database import RocksDB
from diagrams.onprem.network import Etcd
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client
from diagrams.programming.framework import Spring

with Diagram("HikariKeeper Architecture", show=False, direction="TB"):
    client = Client("Client")
    
    with Cluster("HikariKeeper Cluster"):
        with Cluster("Raft Consensus"):
            leader = Server("Leader Node")
            follower1 = Server("Follower Node")
            follower2 = Server("Follower Node")
            
        with Cluster("Metadata Storage"):
            storage = RocksDB("RocksDB")
            
        with Cluster("Discovery Service"):
            discovery = Etcd("Discovery")
            
        with Cluster("Spring Boot Integration"):
            spring = Spring("Spring Boot Starter")
    
    client >> leader
    leader >> follower1
    leader >> follower2
    follower1 >> leader
    follower2 >> leader
    leader >> storage
    follower1 >> storage
    follower2 >> storage
    leader >> discovery
    spring >> leader