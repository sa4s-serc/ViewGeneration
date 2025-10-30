from diagrams import Cluster, Diagram
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.queue import ActiveMQ
from diagrams.programming.flowchart import Action, Decision

with Diagram("PyJailBreak Frontend Architecture", show=False):
    user = User("User")

    with Cluster("Frontend"):
        nginx = Nginx("Nginx")
        user >> nginx

    with Cluster("Backend"):
        server = Server("Backend Server")
        activemq = ActiveMQ("ActiveMQ")

        nginx >> server
        server >> activemq

    with Cluster("Core Functionality"):
        scan_config = Action("Scan Configuration UI")
        payload_mgmt = Action("Payload Management")
        scan_exec = Action("Scan Execution")
        emulation_mode = Action("Emulation Mode")
        configuration = Action("Configuration")
        api_doc = Action("API Documentation")

        server >> scan_config
        server >> payload_mgmt
        server >> scan_exec
        server >> emulation_mode
        server >> configuration
        server >> api_doc

    with Cluster("Decision Points"):
        decision = Decision("Choose Mode")
        emulation_mode >> decision
        decision >> scan_exec