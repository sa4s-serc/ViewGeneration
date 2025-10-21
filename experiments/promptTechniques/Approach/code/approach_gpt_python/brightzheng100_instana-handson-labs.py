from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import API, Kubelet
from diagrams.k8s.compute import Pod
from diagrams.k8s.rbac import User
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Users
from diagrams.onprem.monitoring import Grafana
from diagrams.generic.os import Ubuntu
from diagrams.generic.os import Centos

with Diagram("Instana Hands-on Labs Architecture", show=False, direction="TB"):
    with Cluster("Instana APM Platform"):
        instana_backend = Server("Instana Backend")
        
        with Cluster("Agents and Monitoring"):
            k8s_agent = Kubelet("K8s Agent")
            vm_agent = Kubelet("VM Agent")
            docker_agent = Kubelet("Docker Agent")
            
            instana_backend >> Edge(label="Monitors") >> k8s_agent
            instana_backend >> Edge(label="Monitors") >> vm_agent
            instana_backend >> Edge(label="Monitors") >> docker_agent

    with Cluster("Kubernetes Environment"):
        k8s_api = API("K8s API")
        k8s_node = Pod("K8s Node")
        
        k8s_api >> Edge(label="Schedules") >> k8s_node
        k8s_node >> Edge(label="Runs") >> k8s_agent
        
    with Cluster("VM Environment"):
        centos_vm = Centos("CentOS VM")
        ubuntu_vm = Ubuntu("Ubuntu VM")
        
        centos_vm >> Edge(label="Runs") >> vm_agent
        ubuntu_vm >> Edge(label="Runs") >> vm_agent

    with Cluster("Docker Environment"):
        docker_container = Pod("Docker Container")
        
        docker_container >> Edge(label="Runs") >> docker_agent

    with Cluster("Monitoring and Configuration Tools"):
        grafana = Grafana("Grafana")
        users = Users("Developers")
        
        users >> Edge(label="Accesses") >> grafana
        grafana >> Edge(label="Visualizes") >> instana_backend