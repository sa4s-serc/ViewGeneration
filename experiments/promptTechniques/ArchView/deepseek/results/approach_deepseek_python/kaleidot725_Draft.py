from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.os import Android

with Diagram("Emomemo App Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Presentation Layer"):
        android_app = Android("Android App\n(Jetpack Compose)")
        navigation = Server("Navigation\nCompose")
        text_editor = Server("TextEditor\nComponent")
        
        android_app >> navigation
        android_app >> text_editor
    
    with Cluster("Domain Layer"):
        use_cases = Server("Use Cases")
        view_models = Server("ViewModels\n(MVI Pattern)")
        
        use_cases >> view_models
    
    with Cluster("Data Layer"):
        repositories = Server("Repositories")
        room_db = PostgreSQL("Room Database")
        
        repositories >> room_db
    
    android_app >> view_models
    view_models >> repositories
    use_cases >> repositories
    user >> android_app