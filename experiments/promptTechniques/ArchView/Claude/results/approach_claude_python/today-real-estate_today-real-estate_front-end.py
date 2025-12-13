from diagrams import Diagram, Cluster
from diagrams.programming.framework import Vue
from diagrams.onprem.database import MySQL
from diagrams.programming.framework import Flask
from diagrams.onprem.queue import Kafka
from diagrams.onprem.inmemory import Redis
from diagrams.saas.cdn import Cloudflare
from diagrams.onprem.network import Nginx
from diagrams.onprem.vcs import Github

with Diagram("Today Real Estate Frontend Architecture", show=False, direction="TB"):
    with Cluster("Frontend Layer"):
        vue = Vue("Vue.js App")
        
    with Cluster("Backend Services"):
        api = Flask("REST API")
        db = MySQL("MySQL")
        cache = Redis("Redis Cache")
        queue = Kafka("Kafka")
        
    with Cluster("Infrastructure"):
        cdn = Cloudflare("CDN")
        proxy = Nginx("Nginx")
        repo = Github("Source Code")

    # Frontend connections
    cdn >> vue
    vue >> proxy

    # Backend connections
    proxy >> api
    api >> db
    api >> cache
    api >> queue

    # Development
    repo >> vue
    repo >> api