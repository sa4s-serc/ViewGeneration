from diagrams import Diagram, Cluster
from diagrams.generic.os import Android
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import SQLite
from diagrams.onprem.network import Internet
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Fluentd
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git
from diagrams.onprem.workflow import Airflow

with Diagram("Android Application Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Mobile Layer"):
        android_app = Android("Android App")
        with Cluster("UI Layer"):
            main_activity = Server("MainActivity")
            ribots_adapter = Server("RibotsAdapter")
        
        with Cluster("Presentation Layer"):
            main_presenter = Server("MainPresenter")
        
        with Cluster("Data Layer"):
            data_manager = Server("DataManager")
            with Cluster("Local Storage"):
                database_helper = SQLite("DatabaseHelper")
            with Cluster("Remote API"):
                ribots_service = Server("RibotsService")
        
        with Cluster("Background Services"):
            sync_service = Server("SyncService")
    
    with Cluster("External Services"):
        api_gateway = Server("Ribot API")
        crashlytics = Server("Crashlytics")
    
    with Cluster("Development Tools"):
        dagger = Server("Dagger 2")
        rxjava = Server("RxJava 2")
        timber = Server("Timber")
    
    with Cluster("Testing"):
        unit_tests = Server("Unit Tests")
        ui_tests = Server("UI Tests")
    
    user >> android_app
    
    android_app >> main_activity
    main_activity >> ribots_adapter
    
    main_activity >> main_presenter
    main_presenter >> data_manager
    
    data_manager >> database_helper
    data_manager >> ribots_service
    data_manager >> sync_service
    
    ribots_service >> api_gateway
    android_app >> crashlytics
    
    sync_service >> api_gateway
    sync_service >> database_helper
    
    dagger >> android_app
    rxjava >> android_app
    timber >> android_app
    
    unit_tests >> android_app
    ui_tests >> android_app