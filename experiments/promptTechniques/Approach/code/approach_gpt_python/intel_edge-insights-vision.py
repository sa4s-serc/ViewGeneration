from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.client import Client
from diagrams.programming.framework import JupyterLab

with Diagram("Edge Insights for Vision (EIV) Architecture", show=False):

    user = Client("User")

    with Cluster("EIV Setup"):
        install_script = Server("eiv_install.sh")
        setup_script = Server("eiv_setup.py")
        callbacks_script = Server("eiv_callbacks.sh")
        launch_script = Server("launch_notebooks.sh")
        adl_scripts = Server("adl_*.sh")

        install_script >> Edge(label="calls") >> setup_script
        setup_script >> Edge(label="uses") >> callbacks_script
        launch_script >> Edge(label="starts") >> JupyterLab("Jupyter Notebooks")
        adl_scripts >> Edge(label="enables") >> Server("MIPI Camera Support")

    with Cluster("Docker Environment"):
        docker = Docker("Docker")
        docker_image = Docker("OpenVINO Image")
        docker_image << Edge(label="managed by") << callbacks_script

        docker >> Edge(label="runs") >> docker_image

    with Cluster("Intel Hardware"):
        cpu = Server("CPU")
        igpu = Server("iGPU")
        dgpu = Server("dGPU")

    user >> Edge(label="initiates") >> install_script
    docker_image >> Edge(label="executes on") >> [cpu, igpu, dgpu]