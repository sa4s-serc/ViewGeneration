from diagrams import Diagram, Cluster
from diagrams.generic.os import Ubuntu
from diagrams.programming.framework import Vue
from diagrams.programming.language import JavaScript, Python
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.firebase.develop import Firestore
from diagrams.aws.blockchain import Blockchain
from diagrams.saas.cdn import Cloudflare

with Diagram("FLibra Marketplace Architecture", show=False):
    nuxtjs = Vue("Nuxt.js Frontend")

    with Cluster("Frontend"):
        search_function = JavaScript("SearchFunction.vue")
        item_list = JavaScript("ItemList.vue")
        header_bar = JavaScript("HeaderBar.vue")
        nuxtjs >> [search_function, item_list, header_bar]

    with Cluster("Blockchain Integration"):
        libra = Blockchain("Libra")
        ethereum = Blockchain("Ethereum")
        nuxtjs >> libra
        nuxtjs >> ethereum

    with Cluster("Data Storage"):
        firestore = Firestore("Firestore")
        ipfs = Cloudflare("IPFS")
        elasticsearch = Elasticsearch("Elasticsearch")
        nuxtjs >> firestore
        nuxtjs >> ipfs
        nuxtjs >> elasticsearch

    with Cluster("Backend Components"):
        nodejs = JavaScript("Node.js")
        with Cluster("Modules"):
            search = Python("Search.js")
            registration = Python("Registration.js")
            delete_item = Python("DeleteItem.js")
            nodejs >> [search, registration, delete_item]
            firestore >> nodejs
            elasticsearch >> nodejs

    with Cluster("Database"):
        postgresql = PostgreSQL("PostgreSQL")
        redis = Redis("Redis")
        nodejs >> postgresql
        nodejs >> redis

    ubuntu = Ubuntu("Server")
    nuxtjs >> ubuntu
    nodejs >> ubuntu