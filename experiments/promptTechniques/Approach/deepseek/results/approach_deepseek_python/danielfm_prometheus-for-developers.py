from diagrams import Diagram
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.aggregator import Fluentd
from diagrams.programming.language import Nodejs
from diagrams.onprem.container import Docker

with Diagram("Prometheus Monitoring Architecture", show=False, direction="LR"):
    docker = Docker("Docker Compose")
    
    sample_app = Nodejs("Sample Node.js App")
    prometheus = Prometheus("Prometheus")
    alertmanager = Fluentd("Alertmanager")
    grafana = Grafana("Grafana")
    
    sample_app >> prometheus
    prometheus >> alertmanager
    prometheus >> grafana