from diagrams import Diagram, Cluster
from diagrams.programming.language import Java
from diagrams.onprem.client import Client
from diagrams.onprem.database import Mongodb, Postgresql, Mariadb
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.iac import Ansible
from diagrams.onprem.logging import Rsyslog
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import Kafka

with Diagram("ARGAEL Architecture", direction="TB"):

    client = Client("User")

    with Cluster("ARGAEL Application"):
        java_app = Java("ARGAEL")
        gui = Java("GUI")
        io_manager = Java("IO Manager")
        data_manager = Java("Data Manager")
        report_formatter = Java("Report Formatter")

    with Cluster("Data Storage"):
        jsonl_storage = Mariadb("JSONL Data")
        csv_storage = Postgresql("CSV Data")
        html_storage = Mongodb("HTML Templates")

    with Cluster("Data Processing"):
        argument_annotation = Java("Argument Annotation")
        annotation_evaluation = Java("Annotation Evaluation")
        argument_models = Java("Argument Models")

    client >> gui
    gui >> java_app
    java_app >> io_manager >> data_manager >> report_formatter
    
    io_manager >> jsonl_storage
    io_manager >> csv_storage
    report_formatter >> html_storage

    argument_annotation >> annotation_evaluation
    argument_models >> annotation_evaluation
    annotation_evaluation >> io_manager

    # Additional components
    vcs = Git("Version Control")
    ci_cd = Jenkins("CI/CD")
    monitoring = Prometheus("Monitoring")
    logging = Rsyslog("Logging")
    config_mgmt = Ansible("Config Management")
    containerization = Docker("Containerization")
    web_server = Nginx("Web Server")
    event_queue = Kafka("Event Queue")

    client >> web_server >> java_app
    containerization >> java_app
    config_mgmt >> java_app
    monitoring >> java_app
    logging >> java_app
    vcs >> ci_cd >> java_app
    event_queue >> java_app