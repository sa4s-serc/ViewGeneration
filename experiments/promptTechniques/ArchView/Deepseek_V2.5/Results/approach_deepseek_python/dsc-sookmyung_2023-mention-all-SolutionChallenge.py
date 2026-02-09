from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.generic.os import Android, IOS
from diagrams.programming.language import Kotlin, Swift, Java
from diagrams.generic.database import SQL
from diagrams.gcp.api import Endpoints
from diagrams.gcp.ml import InferenceAPI
from diagrams.firebase.grow import Messaging
from diagrams.gcp.compute import KubernetesEngine

with Diagram("CPR2U System Architecture", show=False, direction="TB"):
    users = User("Users")
    cpr_angels = User("CPR Angels")
    
    with Cluster("Mobile Applications"):
        with Cluster("Android App"):
            android = Android("Android")
            kotlin = Kotlin("Kotlin")
            ml_kit = InferenceAPI("ML Kit")
            firebase_auth = Messaging("Firebase Auth")
            maps = Endpoints("Google Maps")
        
        with Cluster("iOS App"):
            ios = IOS("iOS")
            swift = Swift("Swift")
            tf_lite = InferenceAPI("TensorFlow Lite")
            combine = Swift("Combine")
    
    with Cluster("Backend Services"):
        with Cluster("Spring Boot Backend"):
            spring_boot = Java("Spring Boot")
            auth_service = SQL("Auth Service")
            education_service = SQL("Education Service")
            dispatch_service = SQL("Dispatch Service")
            fcm_service = Messaging("FCM Service")
        
        with Cluster("External Services"):
            firebase = Messaging("Firebase")
            google_maps = Endpoints("Google Maps API")
            gcp = KubernetesEngine("GCP")
    
    users >> android
    users >> ios
    cpr_angels >> android
    cpr_angels >> ios
    
    android >> spring_boot
    ios >> spring_boot
    
    spring_boot >> auth_service
    spring_boot >> education_service
    spring_boot >> dispatch_service
    spring_boot >> fcm_service
    
    auth_service >> firebase
    dispatch_service >> google_maps
    fcm_service >> firebase
    spring_boot >> gcp