from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.database import Mongodb
from diagrams.onprem.network import Consul
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client
from diagrams.generic.storage import Storage

with Diagram("IceFireDB Architecture", show=False, direction="TB") as diag:
    client = Client("Client")

    with Cluster("IceFireDB Core"):
        leveldb = Mongodb("LevelDB")
        uhaha = Consul("Uhaha")

    with Cluster("Distributed SQL Proxy"):
        proxy = Server("IceFireDB-SQLProxy")
        libp2p = Consul("libp2p Network")
        storage = Storage("Pluggable Storage Engines")

    client >> proxy
    proxy >> Edge(label="SQL Queries") >> leveldb
    proxy >> Edge(label="Data Sync") >> libp2p
    proxy >> Edge(label="Storage") >> storage
    uhaha >> Edge(label="Consensus") >> leveldb

diag