from diagrams import Diagram, Cluster
from diagrams.onprem.workflow import Nifi
from diagrams.onprem.database import Zookeeper
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import Postgresql
from diagrams.onprem.database import Mongodb
from diagrams.onprem.database import Cassandra
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Nginx
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Ansible
from diagrams.onprem.iac import Terraform
from diagrams.onprem.network import Envoy
from diagrams.onprem.network import Istio
from diagrams.onprem.compute import Server
from diagrams.onprem.security import Vault
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.client import User

with Diagram("Apache NiFi/Orchsym Runtime Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Web Interface"):
        ui = Nginx("Web UI")
        api = Nifi("REST API")
        ui >> api
    
    with Cluster("Core Framework"):
        with Cluster("Flow Management"):
            flow_controller = Nifi("FlowController")
            process_scheduler = Nifi("ProcessScheduler")
            flow_service = Nifi("StandardFlowService")
            flow_synchronizer = Nifi("FlowSynchronizer")
            
        with Cluster("State Management"):
            state_manager = Nifi("StateManagerProvider")
            zookeeper = Zookeeper("ZooKeeper")
            
        with Cluster("Data Flow"):
            process_session = Nifi("ProcessSession")
            flow_file = Nifi("FlowFile")
            connection = Nifi("Connection")
            queue = Nifi("FlowFileQueue")
    
    with Cluster("Repositories"):
        flowfile_repo = Postgresql("FlowFile\nRepository")
        content_repo = Mongodb("Content\nRepository")
        provenance_repo = Cassandra("Provenance\nRepository")
    
    with Cluster("Security"):
        auth = Vault("Authentication")
        authorizer = Nifi("Authorizer")
        ssl_service = Nifi("SSLContextService")
    
    with Cluster("Controller Services"):
        controller_services = Nifi("ControllerServiceProvider")
    
    with Cluster("Cluster Management"):
        cluster_coordinator = Nifi("ClusterCoordinator")
        cluster_nodes = [Server("Node 1"), Server("Node 2"), Server("Node 3")]
    
    with Cluster("External Integrations"):
        kafka = Kafka("Apache Kafka")
        hadoop = Nifi("Hadoop")
        druid = Nifi("Apache Druid")
        ignite = Nifi("Apache Ignite")
        rabbitmq = Nifi("RabbitMQ")
        couchbase = Nifi("Couchbase")
    
    with Cluster("Orchsym Runtime"):
        branding = Nifi("Branding\nExtension")
        custom_auth = Nifi("Custom Login\nProvider")
        udc = Nifi("Usage Data\nCollection")
    
    user >> ui
    api >> flow_controller
    flow_controller >> process_scheduler
    flow_controller >> flow_service
    flow_controller >> flow_synchronizer
    flow_controller >> state_manager
    state_manager >> zookeeper
    flow_controller >> process_session
    process_session >> flow_file
    flow_file >> connection
    connection >> queue
    
    flow_controller >> flowfile_repo
    flow_controller >> content_repo
    flow_controller >> provenance_repo
    
    flow_controller >> auth
    auth >> authorizer
    auth >> ssl_service
    
    flow_controller >> controller_services
    
    flow_controller >> cluster_coordinator
    cluster_coordinator >> cluster_nodes
    
    flow_controller >> kafka
    flow_controller >> hadoop
    flow_controller >> druid
    flow_controller >> ignite
    flow_controller >> rabbitmq
    flow_controller >> couchbase
    
    flow_controller >> branding
    flow_controller >> custom_auth
    flow_controller >> udc