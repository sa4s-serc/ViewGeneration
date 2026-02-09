from diagrams import Diagram, Cluster
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Github
from diagrams.generic.os import Android

with Diagram("mytaxi_AndroidCI Architecture", show=False):
    with Cluster("CI/CD Environment"):
        github = Github("Android\nProject")
        
        with Cluster("Jenkins Pipeline"):
            jenkins = Jenkins("Jenkins\n2.60.3-alpine")
            
            with Cluster("Build Environment"):
                docker = Docker("Docker Host")
                build = Docker("Android Build\nContainer") 
                sdk = Android("Android SDK")
                
                docker - build
                build - sdk

        # Define the flow
        github >> jenkins >> docker