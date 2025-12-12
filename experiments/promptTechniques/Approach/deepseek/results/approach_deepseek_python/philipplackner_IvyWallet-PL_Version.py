from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.mobile import Android
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.storage import Ceph
from diagrams.onprem.network import Nginx
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki
from diagrams.onprem.tracing import Jaeger

with Diagram("Ivy Wallet Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Mobile Client"):
        mobile = Android("Ivy Wallet App")
        ui_components = [
            Server("Home Screen"),
            Server("Transaction UI"),
            Server("Account UI"),
            Server("Category UI")
        ]
    
    with Cluster("Backend Services"):
        with Cluster("Core Modules"):
            core_services = [
                Server("Transaction\nManagement"),
                Server("Account\nManagement"),
                Server("Category\nManagement"),
                Server("Exchange Rates")
            ]
        
        with Cluster("Advanced Features"):
            advanced_services = [
                Server("Sync Module"),
                Server("Backup Module"),
                Server("Formula Engine")
            ]
        
        with Cluster("Infrastructure"):
            infra_services = [
                Server("Navigation"),
                Server("Design System"),
                Server("Notifications")
            ]
    
    with Cluster("Data Layer"):
        databases = [
            PostgreSQL("Transactions DB"),
            PostgreSQL("Accounts DB"),
            PostgreSQL("Categories DB"),
            Ceph("File Storage")
        ]
    
    with Cluster("Monitoring & CI/CD"):
        monitoring = [
            Grafana("Monitoring"),
            Loki("Logging"),
            Jaeger("Tracing")
        ]
        ci_cd = Jenkins("CI/CD Pipeline")
    
    user >> mobile
    mobile >> ui_components
    ui_components >> core_services
    ui_components >> advanced_services
    core_services >> databases
    advanced_services >> databases
    infra_services >> core_services
    infra_services >> advanced_services
    core_services >> monitoring
    advanced_services >> monitoring
    ci_cd >> core_services
    ci_cd >> advanced_services