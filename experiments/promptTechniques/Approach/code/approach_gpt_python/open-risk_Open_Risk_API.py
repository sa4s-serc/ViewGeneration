from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mongodb
from diagrams.programming.flowchart import Action

with Diagram("Open Risk API Architecture", show=False):
    # Open Risk API
    open_risk_api = Custom("Open Risk API", "./images/api.png")

    # Model Server
    with Cluster("Model Server"):
        model_server = Server("Flask-based Server")
        model_metadata = Action("RDFlib Metadata")
        concentration_library = Action("Concentration Library")

    # Data Server
    with Cluster("Data Server"):
        data_server = Server("Python-Eve Server")
        mongodb = Mongodb("MongoDB")

    # API Explorer (Python Client)
    api_explorer = Client("API Explorer")

    # OpenCPM
    with Cluster("OpenCPM"):
        open_cpm_tools = Action("Concentration Metrics")
        npl_concentration = Action("NPL Concentration Metrics")
        model_definitions = Action("Model Definitions")
        libreoffice_macros = Action("LibreOffice Macros")

    # Connections
    open_risk_api >> model_server
    open_risk_api >> data_server
    model_server >> model_metadata
    model_server >> concentration_library
    data_server >> mongodb
    api_explorer >> open_risk_api
    open_risk_api >> open_cpm_tools
    open_cpm_tools >> npl_concentration
    npl_concentration >> model_definitions
    npl_concentration >> libreoffice_macros