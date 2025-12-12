from diagrams import Diagram, Cluster
from diagrams.onprem.iac import Ansible
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python
from diagrams.programming.language import Bash
from diagrams.onprem.vcs import Git
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.network import Nginx

with Diagram("Edge Insights for Vision Architecture", show=False):
    git = Git("Repository")
    ansible = Ansible("eiv_install.sh")
    docker = Docker("Docker")
    python = Python("eiv_setup.py")
    bash = Bash("scripts/eiv_callbacks.sh")
    jenkins = Jenkins("CI/CD")
    nginx = Nginx("Web Server")

    with Cluster("Core Functionality"):
        install_script = ansible
        setup_script = python
        callback_script = bash

    with Cluster("Documentation & Information"):
        readme = Git("README.md")
        docs = Git("docs/*")

    with Cluster("Docker-Centric Deployment"):
        container = docker

    git >> [install_script, setup_script, callback_script, readme, docs]
    install_script >> [setup_script, callback_script]
    setup_script >> container
    callback_script >> container
    container >> nginx
    [readme, docs] >> nginx
    git >> jenkins
    jenkins >> container