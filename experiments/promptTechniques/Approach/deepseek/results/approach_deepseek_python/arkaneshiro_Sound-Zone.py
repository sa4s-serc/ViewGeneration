from diagrams import Diagram
from diagrams.onprem.client import Users
from diagrams.programming.framework import React
from diagrams.programming.language import Javascript
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.saas.media import Cloudinary

with Diagram("Soundzone Web Application Architecture", show=False, direction="TB"):
    user = Users("User")
    
    frontend = React("React Frontend")
    redux = Javascript("Redux State Management")
    
    backend = Nginx("Node.js/Express Backend")
    database = Postgresql("PostgreSQL Database")
    cloudinary = Cloudinary("Cloudinary Storage")
    
    user >> frontend
    frontend >> redux
    frontend >> backend
    backend >> database
    backend >> cloudinary