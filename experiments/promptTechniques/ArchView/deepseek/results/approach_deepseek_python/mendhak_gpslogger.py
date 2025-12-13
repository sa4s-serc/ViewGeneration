from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.generic.os import Android
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.storage import Ceph
from diagrams.onprem.queue import Kafka
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import FluentBit

with Diagram("GPSLogger Architecture View", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Mobile Layer"):
        android_app = Android("GPSLogger App")
        with Cluster("UI Components"):
            main_activity = Server("Main Activity")
            settings_activity = Server("Settings Activity")
            big_view = Server("Big View Mode")
        
        with Cluster("Background Services"):
            gps_service = Server("GPS Logging Service")
            location_listener = Server("Location Listener")
            notification_service = Server("Notification Service")
    
    with Cluster("Application Layer"):
        with Cluster("Business Logic"):
            preference_helper = Server("Preference Helper")
            app_settings = Server("App Settings")
            session_manager = Server("Session Manager")
            event_bus = Kafka("Event Bus")
        
        with Cluster("Data Processing"):
            file_logger_factory = Server("File Logger Factory")
            with Cluster("File Loggers"):
                gpx_logger = Server("GPX Logger")
                kml_logger = Server("KML Logger")
                csv_logger = Server("CSV Logger")
        
        with Cluster("Upload Services"):
            with Cluster("Upload Managers"):
                google_drive_mgr = Server("Google Drive Manager")
                dropbox_mgr = Server("Dropbox Manager")
                sftp_mgr = Server("SFTP Manager")
                osm_mgr = Server("OSM Manager")
            
            with Cluster("Workers"):
                google_drive_worker = Server("Google Drive Worker")
                dropbox_worker = Server("Dropbox Worker")
                sftp_worker = Server("SFTP Worker")
    
    with Cluster("Data Layer"):
        local_storage = Ceph("Local File Storage")
        preferences_db = Redis("Preferences Cache")
        config_db = PostgreSQL("Configuration DB")
    
    with Cluster("External Services"):
        google_drive = Server("Google Drive")
        dropbox = Server("Dropbox")
        openstreetmap = Server("OpenStreetMap")
        sftp_server = Server("SFTP Server")
        tasker = Server("Tasker Integration")
    
    with Cluster("Infrastructure"):
        with Cluster("CI/CD"):
            github_actions = Jenkins("GitHub Actions")
            fastlane = Server("Fastlane")
        
        with Cluster("Monitoring"):
            prometheus_mon = Prometheus("Prometheus")
            grafana_dash = Grafana("Grafana")
            fluentd_logs = FluentBit("FluentBit")
        
        with Cluster("Documentation"):
            eleventy = Server("Eleventy Docs")
            docker_test = Docker("Test Harness")
    
    user >> android_app
    android_app >> main_activity
    android_app >> settings_activity
    android_app >> big_view
    android_app >> gps_service
    android_app >> notification_service
    
    gps_service >> location_listener
    location_listener >> event_bus
    
    main_activity >> preference_helper
    settings_activity >> preference_helper
    preference_helper >> app_settings
    app_settings >> session_manager
    
    gps_service >> file_logger_factory
    file_logger_factory >> gpx_logger
    file_logger_factory >> kml_logger
    file_logger_factory >> csv_logger
    
    gpx_logger >> local_storage
    kml_logger >> local_storage
    csv_logger >> local_storage
    
    event_bus >> google_drive_mgr
    event_bus >> dropbox_mgr
    event_bus >> sftp_mgr
    event_bus >> osm_mgr
    
    google_drive_mgr >> google_drive_worker
    dropbox_mgr >> dropbox_worker
    sftp_mgr >> sftp_worker
    
    google_drive_worker >> google_drive
    dropbox_worker >> dropbox
    sftp_worker >> sftp_server
    osm_mgr >> openstreetmap
    
    preference_helper >> preferences_db
    app_settings >> config_db
    
    android_app >> tasker
    
    github_actions >> fastlane
    gps_service >> prometheus_mon