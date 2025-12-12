from diagrams import Diagram, Cluster
from diagrams.programming.framework import React
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import Javascript
from diagrams.generic.network import Firewall

with Diagram("Skemi Front-End Architecture", show=False, direction="TB"):
    users = User("Users")
    
    with Cluster("Frontend Layer"):
        frontend = React("React App")
        with Cluster("Components"):
            nav = Javascript("Nav Component")
            login = Javascript("Login Component")
            occasions = Javascript("Occasion Components")
            rosters = Javascript("Roster Components")
            users_comp = Javascript("User Components")
        
        with Cluster("State Management"):
            state_context = Javascript("State Context")
            state_reducer = Javascript("State Reducer")
        
        with Cluster("Services"):
            auth_services = Javascript("Auth Services")
            occasion_services = Javascript("Occasion Services")
            roster_services = Javascript("Roster Services")
            user_services = Javascript("User Services")
        
        with Cluster("Configuration"):
            api_config = Javascript("API Config")
    
    with Cluster("Backend Layer"):
        backend = Nginx("Rails API")
        with Cluster("Data Storage"):
            database = Postgresql("PostgreSQL")
            cache = Redis("Redis Cache")
    
    with Cluster("Security"):
        firewall = Firewall("Firewall")
        jwt_auth = Javascript("JWT Auth")
    
    users >> frontend
    frontend >> nav
    frontend >> login
    frontend >> occasions
    frontend >> rosters
    frontend >> users_comp
    frontend >> state_context
    frontend >> state_reducer
    frontend >> auth_services
    frontend >> occasion_services
    frontend >> roster_services
    frontend >> user_services
    frontend >> api_config
    api_config >> backend
    backend >> database
    backend >> cache
    frontend >> jwt_auth
    users >> firewall
    firewall >> frontend