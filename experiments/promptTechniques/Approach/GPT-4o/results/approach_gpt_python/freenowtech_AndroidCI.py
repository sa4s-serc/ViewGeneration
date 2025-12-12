from diagrams import Diagram, Cluster, Node
from diagrams.custom import Custom
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker

with Diagram("mytaxi_AndroidCI Architecture", show=False):
    jenkins_master = Jenkins("Jenkins Master")
    
    android_sdk = Custom("Android SDK", "./android_sdk_icon.png")  # Placeholder for Android SDK image

    with Cluster("Docker Host"):
        docker_agent = Docker("Docker Agent")
        docker_container = Docker("Build Container")
    
    jenkins_master >> docker_agent
    docker_agent >> docker_container
    docker_container >> android_sdk