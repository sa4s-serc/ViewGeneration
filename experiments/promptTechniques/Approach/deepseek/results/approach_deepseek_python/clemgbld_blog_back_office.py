from diagrams import Diagram
from diagrams.programming.framework import React
from diagrams.programming.language import TypeScript
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import GraphQL
from diagrams.aws.security import Cognito
from diagrams.aws.storage import S3

with Diagram("Blog Back Office Architecture", show=False, direction="TB"):
    user = User("Admin User")
    
    frontend = React("React Frontend")
    typescript = TypeScript("TypeScript")
    redux = React("Redux State")
    router = Nginx("React Router")
    editor = React("Rich Text Editor")
    
    backend = GraphQL("GraphQL API")
    auth = Cognito("Authentication")
    
    database = Postgresql("PostgreSQL")
    cache = Redis("Redis Cache")
    storage = S3("File Storage")
    
    user >> frontend
    frontend >> typescript
    frontend >> redux
    frontend >> router
    frontend >> editor
    
    frontend >> backend
    frontend >> auth
    
    backend >> database
    backend >> cache
    backend >> storage
    auth >> database