from diagrams import Diagram
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.generic.os import Android
from diagrams.aws.general import Client

with Diagram("mytaxi_AndroidCI Architecture", show=False, direction="TB"):
    developer = Client("Developer")
    jenkins = Jenkins("Jenkins\n(2.60.3-alpine)")
    docker = Docker("Docker\n(Build Environment)")
    android_sdk = Android("Android SDK\n(Docker Image)")
    android_project = Android("Android Project")
    build_artifacts = Client("Build Artifacts")

    developer >> jenkins
    jenkins >> docker
    docker >> android_sdk
    android_sdk >> android_project
    android_project >> build_artifacts