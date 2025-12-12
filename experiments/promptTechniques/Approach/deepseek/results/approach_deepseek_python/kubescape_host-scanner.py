from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Fluentbit
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git

with Diagram("Kubescape Host Scanner Architecture", show=False):
    git = Git("Git Repository")
    jenkins = Jenkins("CI/CD Pipeline")
    
    with Cluster("Host Scanner Service"):
        nginx = Nginx("API Gateway")
        
        with Cluster("HTTP Layer"):
            healthz = Server("/healthz")
            readyz = Server("/readyz")
            osrelease = Server("/osrelease")
            kubeletinfo = Server("/kubeletinfo")
        
        with Cluster("Sensor Layer"):
            os_sensor = Docker("OS Sensor")
            network_sensor = Docker("Network Sensor")
            container_sensor = Docker("Container Runtime Sensor")
            kubelet_sensor = Docker("Kubelet Sensor")
        
        with Cluster("Data Layer"):
            postgres = PostgreSQL("Configuration DB")
            redis = Redis("Cache")
    
    with Cluster("Monitoring"):
        prometheus = Prometheus("Metrics")
        grafana = Grafana("Dashboard")
        fluentbit = Fluentbit("Logs")
    
    git >> jenkins
    jenkins >> [healthz, readyz, osrelease, kubeletinfo]
    jenkins >> [os_sensor, network_sensor, container_sensor, kubelet_sensor]
    
    nginx >> [healthz, readyz, osrelease, kubeletinfo]
    healthz >> os_sensor
    readyz >> os_sensor
    osrelease >> os_sensor
    kubeletinfo >> kubelet_sensor
    
    os_sensor >> redis
    network_sensor >> redis
    container_sensor >> redis
    kubelet_sensor >> redis
    
    os_sensor >> postgres
    network_sensor >> postgres
    container_sensor >> postgres
    kubelet_sensor >> postgres
    
    [healthz, readyz, osrelease, kubeletinfo] >> fluentbit
    [os_sensor, network_sensor, container_sensor, kubelet_sensor] >> fluentbit
    postgres >> fluentbit
    
    [healthz, readyz, osrelease, kubeletinfo] >> prometheus
    [os_sensor, network_sensor, container_sensor, kubelet_sensor] >> prometheus
    postgres >> prometheus
    
    prometheus >> grafana
    fluentbit >> grafana