from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.network import Internet
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress
from diagrams.k8s.infra import Node
from diagrams.saas.cdn import Cloudflare
from diagrams.saas.identity import Auth0
from diagrams.generic.database import SQL

with Diagram("Microservices Architecture with Dapr", direction="TB"):

    user = User("User")
    
    with Cluster("Kubernetes Cluster"):
        
        ingress = Ingress("API Gateway")
        
        with Cluster("Microservices"):
            identity_server = Auth0("IdentityServer4")
            product_catalog = Pod("ProductCatalogApi")
            inventory_api = Pod("InventoryApi")
            web_ui = Pod("WebUI")
            dapr = Node("Dapr Sidecar")

        dapr >> Edge(label="Service-to-Service\nCommunication") >> [
            identity_server,
            product_catalog,
            inventory_api
        ]
        
        web_ui >> Edge(label="GraphQL") >> ingress >> [product_catalog, inventory_api]
        
        user >> Edge(label="HTTP(S)") >> web_ui

    with Cluster("Infrastructure"):
        db = SQL("Database")
        ci_cd = Cloudflare("CI/CD Pipeline")
        observability = Server("Observability (Zipkin, Seq)")

    product_catalog >> Edge(label="EF Core") >> db
    inventory_api >> Edge(label="EF Core") >> db
    dapr >> Edge(label="Pub/Sub\nMessaging") >> observability
    
    ci_cd >> Edge(label="Build & Deploy") >> Node("K8s")