from diagrams import Diagram, Cluster
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Prometheus
from diagrams.saas.alerting import Pagerduty
from diagrams.onprem.compute import Server
from diagrams.generic.blank import Blank
from diagrams.aws.general import GenericDatabase, GenericFirewall

with Diagram("Wonko Monitoring and Alerting Service", show=False, direction="TB"):
    with Cluster("Staples SparX Microservices"):
        krikkit = Server("Krikkit")
        eccentrica = Server("Eccentrica")
        other_services = Server("Other Services")
    
    with Cluster("Wonko Service"):
        with Cluster("Core Components"):
            core = Blank("core.clj")
            web_server = Blank("web_server.clj")
            alert = Blank("alert.clj")
            config = Blank("config.clj")
        
        with Cluster("Kafka Integration"):
            kafka_admin = Blank("kafka/admin.clj")
            kafka_consume = Blank("kafka/consume.clj")
            kafka_produce = Blank("kafka/produce.clj")
        
        with Cluster("Prometheus Integration"):
            prometheus_export = Blank("export/prometheus.clj")
            prometheus_create = Blank("export/prometheus/create.clj")
            prometheus_register = Blank("export/prometheus/register.clj")
    
    kafka = Kafka("Kafka")
    prometheus = Prometheus("Prometheus")
    pagerduty = Pagerduty("PagerDuty")
    
    krikkit >> kafka
    eccentrica >> kafka
    other_services >> kafka
    
    kafka >> kafka_consume
    kafka_consume >> core
    core >> alert
    alert >> pagerduty
    
    prometheus_create >> prometheus_register
    prometheus_register >> prometheus_export
    prometheus_export >> web_server
    web_server >> prometheus