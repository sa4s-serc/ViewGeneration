from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, ReplicaSet, Deployment
from diagrams.k8s.network import Service, Ingress
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker

with Diagram("Robotont ROS Architecture", show=False, direction="TB"):
    with Cluster("Hardware Layer"):
        robot = Server("Robotont Robot")
        camera = Server("RealSense D435")

    with Cluster("Core Components"):
        driver = Docker("robotont_driver")
        teleop = Docker("robotont_teleop")
        training = Docker("robotont_training")
        description = Docker("robotont_description")
        sensors = Docker("robotont_sensors")

    with Cluster("Navigation & Perception"):
        cartographer = Docker("Cartographer")
        hector = Docker("Hector Mapping")
        rtab = Docker("RTAB-Map")
        ar_track = Docker("ar_track_alvar")

    with Cluster("Data Processing"):
        laserscan = Docker("laserscan_to_distance")
        movebase = Docker("move_base")
        odometry = Docker("odometry")

    # Hardware connections
    robot >> driver
    camera >> [cartographer, rtab, ar_track]

    # Core component interactions
    driver >> teleop
    driver >> training
    description >> [teleop, training]
    sensors >> laserscan

    # Navigation stack
    laserscan >> movebase
    cartographer >> movebase
    hector >> movebase
    rtab >> movebase
    odometry >> movebase

    # Training connections
    training >> ar_track