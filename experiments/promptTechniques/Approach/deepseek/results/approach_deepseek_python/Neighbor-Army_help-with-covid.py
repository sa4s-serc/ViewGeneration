from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import Nextjs
from diagrams.firebase.develop import Firestore, Functions, Authentication
from diagrams.onprem.compute import Server
from diagrams.saas.communication import Twilio
from diagrams.saas.identity import Auth0
from diagrams.generic.network import Firewall

with Diagram("Neighbor Army Help with COVID Architecture", show=False, direction="TB"):
    users = User("Users")
    
    with Cluster("Frontend"):
        frontend = Nextjs("Next.js App")
        address_input = Nextjs("AddressInput Component")
        auth_component = Nextjs("FirebaseAuth Component")
    
    with Cluster("Backend - Firebase Functions"):
        backend = Functions("Express API")
        
        with Cluster("Services"):
            onfleet_service = Server("Onfleet Service")
            firestore_service = Firestore("Firestore Service")
            sendgrid_service = Auth0("Sendgrid Service")
            twilio_service = Twilio("Twilio Service")
    
    with Cluster("External Services"):
        onfleet = Server("Onfleet API")
        google_maps = Firewall("Google Maps API")
        sendgrid = Auth0("Sendgrid API")
        twilio = Twilio("Twilio API")
    
    auth = Authentication("Firebase Auth")
    database = Firestore("Firestore Database")
    
    users >> frontend
    users >> address_input
    users >> auth_component
    
    frontend >> auth
    frontend >> backend
    frontend >> google_maps
    
    address_input >> google_maps
    auth_component >> auth
    
    backend >> onfleet_service
    backend >> firestore_service
    backend >> sendgrid_service
    backend >> twilio_service
    
    onfleet_service >> onfleet
    firestore_service >> database
    sendgrid_service >> sendgrid
    twilio_service >> twilio
    
    auth >> database