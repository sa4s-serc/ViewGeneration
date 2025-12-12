from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.programming.language import Java
from diagrams.elastic.elasticsearch import Elasticsearch, Logstash, Kibana

with Diagram("System Monitoring with ELK Stack", show=False, direction="LR"):
    agent = Java("Agent\n(SystemInfo, TCPServer)")
    logstash = Logstash("Logstash")
    elasticsearch = Elasticsearch("Elasticsearch")
    kibana = Kibana("Kibana")
    
    agent >> logstash >> elasticsearch >> kibana