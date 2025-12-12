from diagrams import Diagram, Cluster
from diagrams.programming.framework import Vue
from diagrams.firebase.base import Firebase 
from diagrams.onprem.database import PostgreSQL
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.queue import Kafka
from diagrams.firebase.develop import Authentication, Firestore, Functions
from diagrams.generic.blank import Blank

with Diagram("FLibra Marketplace Architecture", show=False):
    
    with Cluster("Frontend"):
        frontend = Vue("Frontend")
        nuxt = Blank("Nuxt.js")

    with Cluster("Backend Services"):
        firebase = Firebase("Firebase")
        auth = Authentication("Authentication")
        db = Firestore("Firestore")
        functions = Functions("Cloud Functions")

    with Cluster("Blockchain Layer"):
        eth = Blank("Ethereum")
        libra = Blank("Libra Network")

    with Cluster("Search & Storage"):
        elastic = Elasticsearch("Elasticsearch")
        postgres = PostgreSQL("PostgreSQL")
        queue = Kafka("Message Queue")

    # Frontend connections
    frontend >> nuxt
    nuxt >> firebase
    nuxt >> eth
    nuxt >> libra

    # Backend connections
    firebase >> auth
    firebase >> db
    firebase >> functions

    # Data flow
    db >> elastic
    db >> postgres
    functions >> queue
    
    # Search flow
    elastic >> nuxt