from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import Python
from diagrams.onprem.network import Internet

with Diagram("Karura Machine Learning Platform Architecture", show=False):
    user = User("Kintone User")
    internet = Internet("Kintone Platform")
    
    with Cluster("Kintone Environment"):
        master_app = Server("Karura Master App")
        client_plugin = Server("Client Plugin")
    
    with Cluster("Karura Server"):
        tornado_server = Server("Tornado Web Server")
        
        with Cluster("Core ML Components"):
            model_builder = Python("Model Builder")
            model_manager = Python("Model Manager")
            dataset = Python("Dataset")
            field_manager = Python("Field Manager")
            feature_builder = Python("Feature Builder")
        
        model_store = PostgreSQL("Model Store")
        environment = Python("Environment")
    
    user >> internet
    internet >> master_app
    internet >> client_plugin
    client_plugin >> tornado_server
    master_app >> tornado_server
    
    tornado_server >> model_builder
    tornado_server >> model_manager
    tornado_server >> dataset
    tornado_server >> field_manager
    tornado_server >> feature_builder
    
    model_builder >> model_store
    model_manager >> model_store
    dataset >> model_store
    field_manager >> model_store
    feature_builder >> model_store
    
    environment >> dataset
    environment >> model_manager