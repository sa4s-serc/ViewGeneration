from diagrams import Diagram
from diagrams.programming.language import Go
from diagrams.onprem.container import Docker
from diagrams.onprem.database import Influxdb
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.logging import Fluentbit
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.workflow import Airflow

with Diagram("qnib_qframe Architecture", show=False, direction="LR"):
    collectors = Go("Collectors")
    filters = Go("Filters")
    handlers = Go("Handlers")
    
    docker_events = Docker("Docker Events")
    file_input = Nginx("File Input")
    tcp_input = Nginx("TCP Input")
    
    grok_filter = Fluentbit("Grok Filter")
    container_inventory = Docker("Container Inventory")
    
    influxdb_output = Influxdb("InfluxDB")
    elasticsearch_output = Elasticsearch("Elasticsearch")
    log_output = Prometheus("Log Output")
    
    qchan = Go("QChan")
    
    docker_events >> collectors
    file_input >> collectors
    tcp_input >> collectors
    
    collectors >> qchan
    qchan >> filters
    
    filters >> grok_filter
    filters >> container_inventory
    
    grok_filter >> qchan
    container_inventory >> qchan
    
    qchan >> handlers
    
    handlers >> influxdb_output
    handlers >> elasticsearch_output
    handlers >> log_output