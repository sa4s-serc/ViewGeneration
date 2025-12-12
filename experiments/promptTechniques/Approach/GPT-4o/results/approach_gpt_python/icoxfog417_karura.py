from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.custom import Custom
from diagrams.programming.language import Python

with Diagram("Karura Architecture", show=False, direction="LR"):
    user = User("Kintone User")

    with Cluster("Kintone Environment"):
        client_plugin = Custom("Karura Client Plugin", "path/to/icon.png")
        master_app = Custom("Karura Master App", "path/to/icon.png")
        user >> client_plugin
        user >> master_app

    with Cluster("Karura Server"):
        server = Server("Tornado Web Server")
        api = Internet("REST API")
        server >> Edge(label="/train") >> api
        server >> Edge(label="/predict") >> api

        with Cluster("Model Building Pipeline"):
            data_extraction = Python("Data Extraction")
            feature_engineering = Python("Feature Engineering")
            model_selection = Python("Model Selection & Training")
            model_evaluation = Python("Model Evaluation")
            model_persistence = Python("Model Persistence")

            data_extraction >> feature_engineering >> model_selection >> model_evaluation >> model_persistence

    security_layer = Internet("Security Layer")
    server << Edge(label="API Requests") << security_layer
    security_layer << Edge(label="Kintone API") << client_plugin
    security_layer << Edge(label="Kintone API") << master_app

    trained_model = Python("Trained Model")
    model_persistence >> trained_model
    trained_model >> Edge(label="Predictions") >> api

    api >> Edge(label="Responses") >> client_plugin
    api >> Edge(label="Responses") >> master_app