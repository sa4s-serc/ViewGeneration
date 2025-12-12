from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.compute import Server
from diagrams.onprem.ci import Jenkins

with Diagram("Gapfish Deployer Architecture", show=False, direction="TB"):
    user = User("Developer")
    
    with Cluster("CLI Interface"):
        depctl = User("depctl CLI")
    
    with Cluster("Web Application"):
        deployer = Server("Deployer Service")
        puma = Server("Puma Web Server")
    
    with Cluster("Configuration Management"):
        config = Postgresql("YAML Config")
        env_vars = Postgresql("Environment Variables")
    
    with Cluster("Core Components"):
        with Cluster("Deployment Logic"):
            deployment = Server("Deployment Handler")
            k8s_handler = Server("Kubernetes Handler")
        
        with Cluster("Event System"):
            event_logger = Server("EventStreamLogger")
            subscribers = Server("Event Subscribers")
    
    with Cluster("External Services"):
        github = Git("GitHub")
        kubernetes = Docker("Kubernetes")
        docker_registry = Docker("Docker Registry")
    
    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        loki = Loki("Loki")
    
    with Cluster("CI/CD Pipeline"):
        codeship = Jenkins("Codeship CI/CD")
        plugins = Server("Plugins")
    
    user >> depctl
    depctl >> deployer
    deployer >> puma
    puma >> deployment
    deployment >> k8s_handler
    deployment >> event_logger
    event_logger >> subscribers
    
    deployment >> config
    deployment >> env_vars
    deployment >> github
    deployment >> kubernetes
    deployment >> docker_registry
    
    codeship >> deployer
    codeship >> plugins
    plugins >> deployment
    
    deployer >> prometheus
    puma >> prometheus
    deployment >> prometheus
    k8s_handler >> prometheus
    prometheus >> grafana
    
    deployer >> loki
    puma >> loki
    deployment >> loki
    event_logger >> loki