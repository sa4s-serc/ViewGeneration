from diagrams import Diagram, Cluster
from diagrams.programming.language import Javascript, NodeJS
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.database import Mongodb 
from diagrams.onprem.network import Nginx

with Diagram("Node.js/Express Learning Architecture", show=False):
    with Cluster("Core Runtime"):
        nodejs = NodeJS("Node.js Runtime")
        js = Javascript("Async JavaScript\n(Promises)")

    with Cluster("Infrastructure"):
        nginx = Nginx("Reverse Proxy")
        mongo = Mongodb("Database")
        mq = Rabbitmq("Message Queue")
    
    # Web Layer
    nginx >> nodejs

    # Core Application Flow  
    nodejs >> js
    nodejs >> mongo
    nodejs >> mq

    # Data Flow
    mongo >> mq