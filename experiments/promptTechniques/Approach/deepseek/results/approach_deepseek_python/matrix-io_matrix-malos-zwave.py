from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.queue import Zeromq
from diagrams.onprem.inmemory import Memcached
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.iac import Ansible
from diagrams.onprem.vcs import Git
from diagrams.onprem.logging import Fluentbit
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.database import Mongodb
from diagrams.onprem.security import Vault
from diagrams.onprem.workflow import Airflow

with Diagram("MATRIX MALOS Z-Wave Architecture", show=False):
    with Cluster("MATRIX Hardware"):
        creator = Server("MATRIX Creator/Voice")
        zwave_module = Server("Z-Wave Module")
    
    with Cluster("MALOS Core"):
        malos_core = Docker("MALOS Core")
    
    with Cluster("Z-Wave Driver"):
        zwave_driver = Docker("malos_zwave")
        zip_gateway = Server("Z/IP Gateway")
    
    with Cluster("Communication"):
        zmq = Zeromq("ZeroMQ")
        protobuf = Server("Protocol Buffers")
    
    with Cluster("Device Management"):
        add_node = Docker("addnode.js")
        list_nodes = Docker("list.js")
        remove_node = Docker("removenode.js")
    
    with Cluster("Security"):
        security = Vault("Z-Wave Security")
    
    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
    
    with Cluster("Build & Deployment"):
        drone = Jenkins("Drone CI")
        cmake = Server("CMake")
        debian = Server("Debian Package")

    creator >> zwave_module
    zwave_module >> zip_gateway
    zip_gateway >> zwave_driver
    zwave_driver >> malos_core
    malos_core >> zmq
    zmq >> [add_node, list_nodes, remove_node]
    protobuf >> [zwave_driver, malos_core]
    security >> zwave_driver
    zwave_driver >> prometheus
    prometheus >> grafana
    drone >> cmake
    cmake >> debian
    debian >> zwave_driver