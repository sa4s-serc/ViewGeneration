from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.programming.framework import React
from diagrams.programming.language import Javascript
from diagrams.saas.analytics import GoogleAnalytics360
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import Postgresql
from diagrams.saas.search import ElasticsearchService
from diagrams.programming.framework import Nodejs

with Diagram("Knowledge Graph Visualization Application", show=False):
    user = Custom("User", "./user.png")
    
    with Cluster("Frontend"):
        react_app = React("React App")
        redux = Javascript("Redux")
        flatpickr = Javascript("Flatpickr")
        materialize = Custom("Materialize CSS", "./materialize.png")
        sigma_js = Custom("Sigma.js", "./sigmajs.png")

        user >> react_app
        react_app >> Edge(label="State Management") >> redux
        react_app >> Edge(label="Date Picker") >> flatpickr
        react_app >> Edge(label="UI Components") >> materialize
        react_app >> Edge(label="Graph Rendering") >> sigma_js

    with Cluster("Backend"):
        nodejs = Nodejs("Node.js")
        elasticsearch = ElasticsearchService("Elasticsearch")
        redis = Redis("Redis")
        postgresql = Postgresql("PostgreSQL")
        
        react_app >> Edge(label="API Calls") >> nodejs
        nodejs >> Edge(label="Query") >> elasticsearch
        nodejs >> Edge(label="Cache") >> redis
        nodejs >> Edge(label="Store") >> postgresql

    google_analytics = Custom("Google Analytics", "./google_analytics.png")
    react_app >> Edge(label="Track") >> google_analytics