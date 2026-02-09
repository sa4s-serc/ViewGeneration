from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker
from diagrams.onprem.compute import Server
from diagrams.aws.security import Cognito
from diagrams.aws.network import APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.programming.framework import Vue
from diagrams.generic.blank import Blank

with Diagram("Gran Book Application Architecture", show=False, direction="TB"):
    user = User("End User")
    admin_user = User("Admin User")
    
    with Cluster("Web Admin Panel"):
        nuxt_app = Blank("Nuxt.js App")
        vue_components = Vue("Vue Components")
        vuex_store = Server("Vuex Store")
        vuetify = Blank("Vuetify UI")
        
        nuxt_app >> vue_components
        nuxt_app >> vuex_store
        nuxt_app >> vuetify
    
    with Cluster("Backend Services"):
        with Cluster("API Gateway"):
            api_gateway = APIGateway("API Gateway")
            auth_handler = Lambda("Auth Handler")
            routing_handler = Lambda("Routing Handler")
            
            api_gateway >> auth_handler
            api_gateway >> routing_handler
        
        with Cluster("Microservices"):
            book_service = Server("Book Service")
            user_service = Server("User Service")
            chat_service = Server("Chat Service")
        
        with Cluster("Authentication"):
            firebase_auth = Cognito("Firebase Auth")
            auth_service = Server("Auth Service")
            
            firebase_auth >> auth_service
    
    with Cluster("Data Layer"):
        postgresql = PostgreSQL("PostgreSQL")
        redis_cache = Redis("Redis Cache")
        s3_storage = S3("Image Storage")
    
    with Cluster("Infrastructure"):
        docker_container = Docker("Docker Container")
        nginx_proxy = Nginx("Nginx Proxy")
        
        docker_container >> nginx_proxy
    
    user >> nuxt_app
    admin_user >> nuxt_app
    
    nuxt_app >> api_gateway
    api_gateway >> book_service
    api_gateway >> user_service
    api_gateway >> chat_service
    api_gateway >> auth_service
    
    book_service >> postgresql
    user_service >> postgresql
    chat_service >> postgresql
    
    book_service >> redis_cache
    user_service >> redis_cache
    
    book_service >> s3_storage
    user_service >> s3_storage
    
    auth_service >> firebase_auth
    
    nuxt_app >> docker_container
    api_gateway >> docker_container
    book_service >> docker_container
    user_service >> docker_container
    chat_service >> docker_container
    auth_service >> docker_container