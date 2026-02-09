from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import React
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MySQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.monitoring import Grafana, Prometheus

with Diagram("Algorithm Visualization Application Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        frontend = React("React Application")
        with Cluster("React Components"):
            map_component = React("Map.js")
            sidebar = React("Sidebar.js")
            graph_svg = React("GraphSVG.js")
            graph_table = React("GraphTable.js")
            panel = React("Panel.js")
            event_proxy = React("eventProxy.js")
        
        frontend >> [map_component, sidebar, graph_svg, graph_table, panel, event_proxy]
    
    with Cluster("Backend Layer"):
        backend = Server("Node.js Server")
        with Cluster("Backend Components"):
            routes = Server("routes/index.js")
            users = Server("routes/users.js")
            auth = Server("modules/Authorize.js")
            user_module = Server("modules/User.js")
        
        backend >> [routes, users, auth, user_module]
    
    with Cluster("External Services"):
        maps_api = Nginx("Baidu Maps API")
        algorithms = Docker("C++ Algorithms")
    
    with Cluster("Data Layer"):
        database = MySQL("MySQL Database")
        session_store = Redis("Session Store")
    
    with Cluster("Infrastructure"):
        with Cluster("Monitoring"):
            grafana = Grafana("Grafana")
            prometheus = Prometheus("Prometheus")
        
        with Cluster("CI/CD"):
            jenkins = Jenkins("Jenkins")
    
    user >> frontend
    frontend >> backend
    backend >> maps_api
    backend >> algorithms
    backend >> database
    backend >> session_store
    backend >> grafana
    backend >> prometheus
    jenkins >> frontend
    jenkins >> backend