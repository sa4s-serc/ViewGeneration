from diagrams import Diagram
from diagrams.programming.flowchart import Document
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.programming.framework import FastAPI
from diagrams.onprem.container import Docker
from diagrams.onprem.database import PostgreSQL
from diagrams.custom import Custom

with Diagram("FastCGI Function Handler Framework Architecture", show=False, direction="LR"):
    
    # Web Server
    nginx = Nginx("Nginx/Apache\nFastCGI Server")
    
    # Core Framework Components
    handler = Document("ffunc_handler")
    config = Document("ffunc_config_t")
    pool = Document("ffunc_pool")
    session = Document("ffunc_session_t")
    
    # Application Components
    app = FastAPI("Function Handlers")
    docker = Docker("Container Runtime")
    db = PostgreSQL("Database\n(Optional)")

    # Connect components
    nginx >> handler
    handler >> app
    config >> handler
    pool >> handler
    session >> handler
    app >> db
    docker - app

    # Add notes
    # The handler manages request processing and function mapping
    # Config defines server parameters and function mappings
    # Memory pool manages efficient allocation/deallocation
    # Session tracks request context