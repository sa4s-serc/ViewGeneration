from diagrams import Diagram, Cluster, Edge
from diagrams.generic.os import Android
from diagrams.generic.storage import Storage
from diagrams.generic.device import Mobile
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.iac import Terraform
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.vcs import Github
from diagrams.programming.language import Java

with Diagram("GPSLogger Architecture Overview", show=False, direction="TB"):
    user = User("User")

    with Cluster("Mobile Application"):
        gpslogger_app = Android("GPSLogger App")
        gps_service = Mobile("GPSLoggingService")
        ui = Mobile("UI")
        event_bus = Mobile("Event Bus")
        notification = Mobile("Notifications")
        background_processing = Mobile("WorkManager")

        gps_service >> Edge(label="logs GPS data") >> Storage("Device Storage")
        gps_service >> Edge(label="uploads logs") >> [Nginx("OpenStreetMap"), Nginx("Google Drive"), Nginx("Dropbox")]

        ui >> Edge(label="User interacts") >> gpslogger_app
        gpslogger_app >> Edge(label="Displays UI") >> ui
        gpslogger_app >> Edge(label="Background GPS logging") >> gps_service
        gpslogger_app >> Edge(label="Handles Notifications") >> notification
        gpslogger_app >> Edge(label="Manages Preferences") >> Storage("SharedPreferences")
        gpslogger_app >> Edge(label="Event-driven Updates") >> event_bus
        gpslogger_app >> Edge(label="Background Tasks") >> background_processing

    with Cluster("External Services"):
        ext_services = [Nginx("SFTP"), Nginx("FTP"), Nginx("OwnCloud"), Nginx("HTTP/HTTPS")]

    gps_service >> Edge(label="uploads data") >> ext_services
    
    with Cluster("CI/CD Pipeline"):
        github = Github("Source Code")
        github_actions = GithubActions("CI/CD")
        terraform = Terraform("Infrastructure as Code")
        
        github >> Edge(label="Triggers") >> github_actions
        github_actions >> Edge(label="Deploys") >> terraform
        terraform >> Edge(label="Provisions") >> Server("Application Server")

    user >> Edge(label="Uses") >> gpslogger_app