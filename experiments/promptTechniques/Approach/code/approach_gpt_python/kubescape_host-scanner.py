from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Users

with Diagram("Kubescape Host Scanner Architecture", show=False):
    user = Users("User")

    with Cluster("Host Scanner Service"):
        api_server = Nginx("HTTP API Server")
        negroni_middleware = Custom("Negroni Middleware", "./icons/negroni.png")
        api_server >> negroni_middleware

        with Cluster("Sensor Functions"):
            os_sensor = Custom("OS Details", "./icons/os.png")
            network_sensor = Custom("Network Config", "./icons/network.png")
            container_runtime_sensor = Custom("Container Runtime", "./icons/container.png")
            kubelet_sensor = Custom("Kubelet Info", "./icons/kubelet.png")
            control_plane_sensor = Custom("Control Plane", "./icons/controlplane.png")
            security_sensor = Custom("Security Hardening", "./icons/security.png")
            cloud_sensor = Custom("Cloud Provider", "./icons/cloud.png")

        negroni_middleware >> [os_sensor, network_sensor, container_runtime_sensor,
                               kubelet_sensor, control_plane_sensor, security_sensor, cloud_sensor]

    with Cluster("Deployment"):
        k8s_daemonset = Custom("K8s DaemonSet", "./icons/k8s.png")
        docker_image = Docker("Docker Image")

    user >> api_server
    api_server >> k8s_daemonset
    k8s_daemonset >> docker_image