from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git
from diagrams.generic.device import Mobile
from diagrams.generic.compute import Rack

with Diagram("Robotont ROS Package Architecture", show=False, direction="TB"):
    user = User("Operator")
    
    with Cluster("Robot Control"):
        teleop = Server("robotont_teleop")
        driver = Server("robotont_driver")
        hardware = Rack("Robotont Hardware")
        
    with Cluster("Simulation"):
        gazebo = Server("Gazebo Simulation")
        
    with Cluster("Perception & Mapping"):
        mapping = Server("Cartographer/Hector")
        ar_tracking = Server("AR Tag Tracking")
        realsense = Mobile("Realsense D435")
        
    with Cluster("Navigation"):
        navigation = Server("move_base")
        
    with Cluster("Sensors"):
        laserscan = Server("robotont_sensors")
        laserscan_processor = Server("LaserScan Processing")
        
    with Cluster("Training"):
        training = Server("robotont_training")
        
    with Cluster("Description"):
        description = Server("robotont_description")
        
    with Cluster("Monitoring"):
        monitoring = Prometheus("ROS Monitoring")
        tf = Server("TF Transformations")
        
    with Cluster("CI/CD"):
        ci_cd = Jenkins("CI/CD Pipeline")
        version_control = Git("Version Control")
        container_registry = Docker("Container Registry")

    user >> teleop
    teleop >> driver
    driver >> hardware
    teleop >> gazebo
    
    realsense >> mapping
    realsense >> ar_tracking
    mapping >> navigation
    ar_tracking >> training
    
    laserscan >> laserscan_processor
    laserscan_processor >> navigation
    
    description >> gazebo
    description >> hardware
    
    teleop >> monitoring
    driver >> monitoring
    navigation >> monitoring
    mapping >> monitoring
    tf >> monitoring
    
    version_control >> ci_cd
    ci_cd >> container_registry
    container_registry >> teleop
    container_registry >> driver
    container_registry >> gazebo