from diagrams import Diagram
from diagrams.programming.language import Python
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker

with Diagram("Architectural View", show=False):
    nginx = Nginx("Web Server")
    app = Python("Application")
    db = PostgreSQL("Database")
    ci_cd = Jenkins("CI/CD")
    container = Docker("Container")
    
    nginx >> app >> db
    ci_cd >> container
    container >> app