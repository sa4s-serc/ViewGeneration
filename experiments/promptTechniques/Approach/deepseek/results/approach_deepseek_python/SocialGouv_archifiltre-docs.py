from diagrams import Diagram
from diagrams.programming.language import TypeScript, JavaScript
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Celery
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki
from diagrams.onprem.tracing import Jaeger

with Diagram("Archifiltre Desktop Application Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Diagram("Frontend Layer"):
        react_app = TypeScript("React App")
        redux = JavaScript("Redux State")
        i18n = JavaScript("i18next")
        
        react_app >> redux
        react_app >> i18n
    
    with Diagram("Backend Layer"):
        electron_main = TypeScript("Electron Main")
        async_workers = Celery("Async Workers")
        file_processor = Server("File Processor")
        hash_calculator = Server("Hash Calculator")
        export_services = Server("Export Services")
        
        electron_main >> async_workers
        async_workers >> file_processor
        async_workers >> hash_calculator
        async_workers >> export_services
    
    with Diagram("Data Layer"):
        vfs = PostgreSQL("Virtual File System")
        metadata_db = PostgreSQL("Metadata Store")
        cache = Redis("Cache")
        
        file_processor >> vfs
        hash_calculator >> vfs
        export_services >> vfs
        export_services >> metadata_db
        async_workers >> cache
    
    with Diagram("Monitoring & Analytics"):
        sentry = Grafana("Sentry")
        matomo = Loki("Matomo")
        monitoring = Jaeger("Monitoring")
        
        react_app >> sentry
        electron_main >> sentry
        react_app >> matomo
        electron_main >> monitoring
    
    with Diagram("External Services"):
        update_service = Nginx("Electron Updater")
        font_service = Server("Font Service")
        
        electron_main >> update_service
        react_app >> font_service
    
    # Connections between layers
    user >> react_app
    react_app >> electron_main
    electron_main >> vfs
    electron_main >> metadata_db