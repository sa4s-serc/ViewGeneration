from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.vcs import Github, Gitlab
from diagrams.k8s.compute import Pod
from diagrams.k8s.group import Namespace
from diagrams.k8s.others import CRD
from diagrams.onprem.security import Vault

with Diagram("Git Auth Proxy Architecture", show=False, direction="TB"):
    git_clients = User("Git Clients")
    
    with Cluster("Kubernetes Cluster"):
        with Cluster("git-auth-proxy Namespace"):
            proxy = Nginx("Git Auth Proxy")
            metrics = Nginx("Metrics Endpoint")
            
        with Cluster("Application Namespaces"):
            with Cluster("App Namespace 1"):
                app1_pod = Pod("Application Pod")
                app1_secret = CRD("Git Token Secret")
            
            with Cluster("App Namespace 2"):
                app2_pod = Pod("Application Pod")
                app2_secret = CRD("Git Token Secret")
    
    github = Github("GitHub")
    azure_devops = Gitlab("Azure DevOps")
    config = Vault("Configuration")
    
    git_clients >> proxy
    proxy >> github
    proxy >> azure_devops
    proxy >> config
    proxy >> metrics
    proxy >> app1_secret
    proxy >> app2_secret
    app1_secret >> app1_pod
    app2_secret >> app2_pod
    app1_pod >> proxy
    app2_pod >> proxy