from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.custom import Custom
from diagrams.onprem.container import Docker
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mongodb
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import React
from diagrams.programming.language import Python

with Diagram("Lyrics Sentiment Classification Architecture", show=False):
    user = User("User")

    with Cluster("Frontend"):
        react_ui = React("React UI")

    with Cluster("Backend"):
        fastapi_backend = Python("FastAPI")
        cnn_model = Server("CNN Model")
        genius_api = Custom("LyricsGenius API", "./resources/genius_api.png")
        
    with Cluster("Data Storage"):
        es_db = Custom("Elasticsearch", "./resources/elasticsearch.png")

    docker_compose = Docker("Docker Compose")

    user >> react_ui >> fastapi_backend
    fastapi_backend >> cnn_model
    fastapi_backend >> genius_api
    fastapi_backend >> es_db
    es_db >> fastapi_backend

    docker_compose - react_ui
    docker_compose - fastapi_backend
    docker_compose - es_db