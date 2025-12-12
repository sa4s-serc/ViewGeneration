from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Mongodb
from diagrams.onprem.compute import Server
from diagrams.onprem.storage import Ceph
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki
from diagrams.onprem.tracing import Jaeger
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.vcs import Git

with Diagram("Architecture View", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Frontend"):
        frontend = Nginx("Web Server")
    
    with Cluster("Application"):
        app = Server("Application Server")
    
    with Cluster("Data Layer"):
        db = Mongodb("Database")
        storage = Ceph("Storage")
    
    with Cluster("Monitoring"):
        monitoring = Grafana("Monitoring")
        logging = Loki("Logging")
        tracing = Jaeger("Tracing")
    
    with Cluster("CI/CD"):
        ci_cd = Jenkins("CI/CD")
        container = Docker("Container")
        iac = Terraform("Infrastructure")
        vcs = Git("Version Control")
    
    user >> frontend >> app
    app >> db
    app >> storage
    app >> monitoring
    app >> logging
    app >> tracing
    vcs >> ci_cd >> container >> iac