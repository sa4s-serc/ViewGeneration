from diagrams import Diagram, Cluster
from diagrams.aws.general import Client
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python, Cpp
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL

with Diagram("Zswag Architecture", show=False, direction="LR"):
    client = Client("API Client")

    with Cluster("Zswag Components"):
        generator = Python("zswag.gen\nOpenAPI Generator")
        server = Flask("OAServer\n(Flask/Connexion)")
        pyclient = Python("Python OAClient")
        cppclient = Cpp("C++ OAClient")
        db = PostgreSQL("Zserio Services")

    client >> server
    generator >> server
    client >> pyclient
    client >> cppclient
    pyclient >> server
    cppclient >> server
    server >> db