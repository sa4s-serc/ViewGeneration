from diagrams import Diagram
from diagrams.generic.device import Mobile
from diagrams.onprem.compute import Server
from diagrams.programming.language import Python
from diagrams.aws.mobile import APIGateway
from diagrams.gcp.compute import Functions
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.os import Windows
from diagrams.generic.blank import Blank

with Diagram("Warehouse Robot Simulation Architecture", show=False, direction="TB"):
    user = Mobile("User")
    
    web_interface = APIGateway("Web Interface")
    
    with Diagram("Simulation Layer"):
        unity_env = Windows("Unity Environment")
        coppelia_sim = Server("CoppeliaSim")
        
    with Diagram("Control Layer"):
        robot_control = Python("Robot Control")
        path_planning = Python("Path Planning")
        ocr_pipeline = Python("OCR Pipeline")
        
    with Diagram("Cloud Services"):
        speech_to_text = Functions("Speech-to-Text")
        
    with Diagram("Data Layer"):
        config_db = PostgreSQL("Configuration DB")
        cache = Redis("Cache")
    
    user >> web_interface
    web_interface >> speech_to_text
    web_interface >> unity_env
    unity_env >> coppelia_sim
    coppelia_sim >> robot_control
    robot_control >> path_planning
    robot_control >> ocr_pipeline
    robot_control >> config_db
    robot_control >> cache
    speech_to_text >> robot_control