from diagrams import Diagram
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import Flask
from diagrams.onprem.network import Nginx

with Diagram("Open Risk API Architecture", show=False, direction="LR"):
    api_explorer = Client("API Explorer\n(Python Client)")
    
    with Diagram("Open Risk API"):
        with Diagram("Model Server"):
            flask_server = Flask("Flask Server")
            rdflib = Server("RDFlib")
            concentration_lib = Server("Concentration\nMetrics Library")
            
            flask_server >> rdflib
            flask_server >> concentration_lib
        
        with Diagram("Data Server"):
            python_eve = Server("Python-Eve")
            mongodb = MongoDB("MongoDB")
            python_eve >> mongodb
        
        with Diagram("OpenCPM"):
            npl_concentration = Server("NPL Concentration\nMetrics")
            compute_engine = Server("Compute Engine")
            npl_concentration >> compute_engine
    
    api_explorer >> flask_server
    api_explorer >> python_eve
    api_explorer >> npl_concentration
    
    flask_server >> python_eve
    npl_concentration >> python_eve