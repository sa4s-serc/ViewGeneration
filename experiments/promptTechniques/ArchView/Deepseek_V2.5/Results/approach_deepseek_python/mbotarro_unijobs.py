from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.programming.framework import React
from diagrams.onprem.database import PostgreSQL
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.programming.language import Go

with Diagram("UniJobs Application Architecture", show=False, direction="TB"):
    user = User("Student/User")
    
    frontend = React("React Native Frontend")
    
    backend = Go("Go Backend")
    
    postgresql = PostgreSQL("PostgreSQL Database")
    elasticsearch = Elasticsearch("Elasticsearch")
    
    user >> frontend
    frontend >> backend
    backend >> postgresql
    backend >> elasticsearch