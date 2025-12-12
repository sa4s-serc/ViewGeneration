from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import Celery
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.storage import Ceph
from diagrams.programming.language import Python
from diagrams.onprem.workflow import Airflow

with Diagram("YouTube-dl-nas Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Web Interface"):
        web_server = Nginx("Bottle Web Server")
        auth = Server("Authentication")
        templates = Ceph("HTML Templates")
        static_files = Ceph("Static Files")
        
    with Cluster("API Layer"):
        rest_api = Server("REST API")
        
    with Cluster("Queue Management"):
        queue = Celery("Download Queue")
        worker = Server("Download Worker")
        
    with Cluster("Real-time Communication"):
        websocket = Server("WebSocket Server")
        
    with Cluster("Download Services"):
        yt_dlp = Python("yt-dlp")
        youtube_dl = Python("youtube-dl")
        
    with Cluster("Storage"):
        downloads = Ceph("Download Folder")
        auth_file = Ceph("Auth.json")
        
    with Cluster("Scheduling"):
        scheduler = Airflow("Update Scheduler")
        
    user >> web_server
    user >> rest_api
    web_server >> auth
    web_server >> templates
    web_server >> static_files
    web_server >> websocket
    rest_api >> queue
    queue >> worker
    worker >> yt_dlp
    worker >> youtube_dl
    worker >> downloads
    websocket >> user
    scheduler >> yt_dlp
    scheduler >> youtube_dl
    auth >> auth_file