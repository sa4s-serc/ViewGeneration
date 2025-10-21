from diagrams import Diagram, Cluster, Edge
from diagrams.programming.framework import Vue
from diagrams.onprem.client import Client
from diagrams.generic.storage import Storage
from diagrams.onprem.compute import Server
from diagrams.onprem.analytics import Elasticsearch as Elastic
from diagrams.generic.blockchain import Blockchain

with Diagram("FLibra Marketplace Architecture", show=False, direction="LR"):
    client = Client("User")

    with Cluster("Frontend (Nuxt.js)"):
        nuxt = Vue("Nuxt.js App")
        nuxt - Edge(label="Vuex") - Vue("State Management")

    with Cluster("Blockchain Integration"):
        libra = Blockchain("Libra")
        ethereum = Blockchain("Ethereum")
        smart_contracts = Server("Smart Contracts")

    with Cluster("Data Storage"):
        firestore = Storage("Firestore")
        ipfs = Storage("IPFS")
        elasticsearch = Elastic("Elasticsearch")

    client >> nuxt

    nuxt >> Edge(label="Libra Transactions") >> libra
    nuxt >> Edge(label="Ethereum Interactions") >> ethereum
    ethereum >> Edge(label="Deploy/Execute") >> smart_contracts

    nuxt >> Edge(label="Store/Retrieve Data") >> firestore
    nuxt >> Edge(label="Upload/Download") >> ipfs

    with Cluster("Elasticsearch Integration"):
        app = Server("App.js")
        search = Server("Search.js")
        registration = Server("Registration.js")
        delete_item = Server("DeleteItem.js")

    nuxt >> Edge(label="Search") >> elasticsearch
    app >> Edge(label="Sync with Firestore") >> elasticsearch
    app >> [search, registration, delete_item]

    firestore >> Edge(label="Real-time Sync") >> app