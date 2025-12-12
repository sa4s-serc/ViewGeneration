from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Ansible
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.logging import Fluentbit
from diagrams.onprem.security import Vault

with Diagram("Edge Insights for Vision Architecture", show=False):
    user = User("End User")
    
    with Cluster("Installation & Setup Layer"):
        install_script = Server("eiv_install.sh")
        setup_script = Server("eiv_setup.py")
        callbacks = Server("eiv_callbacks.sh")
        
    with Cluster("Docker Environment"):
        docker = Docker("Docker Container")
        notebooks = Server("Jupyter Notebooks")
        openvino_apps = Server("OpenVINO Applications")
        
    with Cluster("Hardware Layer"):
        with Cluster("Intel Hardware"):
            cpu = Server("CPU")
            igpu = Server("iGPU")
            dgpu = Server("dGPU")
            mipi_camera = Server("MIPI Camera")
        
    with Cluster("Configuration & Drivers"):
        graphics_drivers = Server("Graphics Drivers")
        kernel_build = Server("Custom Kernel")
        ipu_library = Server("IPU Library")
        
    with Cluster("Supporting Services"):
        monitoring = Prometheus("Monitoring")
        logging = Fluentbit("Logging")
        config_mgmt = Ansible("Configuration")
        security = Vault("Security")
        
    user >> install_script
    install_script >> setup_script
    setup_script >> callbacks
    callbacks >> docker
    docker >> notebooks
    docker >> openvino_apps
    openvino_apps >> cpu
    openvino_apps >> igpu
    openvino_apps >> dgpu
    openvino_apps >> mipi_camera
    callbacks >> graphics_drivers
    callbacks >> kernel_build
    callbacks >> ipu_library
    graphics_drivers >> igpu
    graphics_drivers >> dgpu
    kernel_build >> mipi_camera
    ipu_library >> mipi_camera
    docker >> monitoring
    docker >> logging
    callbacks >> config_mgmt
    callbacks >> security