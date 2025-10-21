from diagrams import Diagram, Cluster, Edge
from diagrams.aws.mobile import APIGateway
from diagrams.aws.security import Cognito
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.generic.device import Mobile
from diagrams.onprem.iac import Ansible

with Diagram("Hypertrack Live App Architecture", show=False, direction="LR"):
    mobile = Mobile("Android App")
    
    with Cluster("App Module"):
        hypertrack_sdk = APIGateway("HyperTrack SDK")
        google_maps = APIGateway("Google Maps")
        geofence_adapter = APIGateway("Geofence API Adapter")
        branch_io = APIGateway("Branch.io Deep Linking")

    with Cluster("Backend Module"):
        backend_server = Server("Backend Server")
        hypertrack_api = APIGateway("HyperTrack Trips API")
        retrofit = APIGateway("Retrofit")
        cognito_client = Cognito("AWS Cognito")
        ansible = Ansible("BackendClientFactory")
        
    mobile >> Edge(label="uses") >> hypertrack_sdk
    mobile >> Edge(label="displays locations") >> google_maps
    mobile >> Edge(label="manages geofences") >> geofence_adapter
    mobile >> Edge(label="handles deep links") >> branch_io
    
    backend_server >> Edge(label="API Calls") >> hypertrack_api
    backend_server >> Edge(label="Authenticates") >> cognito_client
    backend_server >> Edge(label="Uses") >> retrofit
    backend_server >> Edge(label="Factory Pattern") >> ansible

    hypertrack_sdk >> Edge(label="communicates with") >> backend_server
    cognito_client >> Edge(label="provides auth") >> mobile