from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

with Diagram("Robotont ROS Package Architecture", show=False, direction="TB"):
    with Cluster("Robotont Package"):
        driver = Custom("robotont_driver", "./icons/ros.png")
        teleop = Custom("robotont_teleop", "./icons/ros.png")
        training = Custom("robotont_training", "./icons/ros.png")
        description = Custom("robotont_description", "./icons/ros.png")
        sensors = Custom("robotont_sensors", "./icons/ros.png")

    with Cluster("ROS Communication"):
        pub_sub = Custom("Publisher-Subscriber", "./icons/topic.png")
        param_server = Custom("Parameter Server", "./icons/parameter.png")

    driver >> Edge(label="Serial Communication") >> teleop
    teleop >> Edge(label="Teleoperation Commands") >> driver
    training >> Edge(label="Training Exercises") >> teleop
    description >> Edge(label="URDF Models") >> sensors
    sensors >> Edge(label="LaserScan Data") >> driver

    driver >> Edge(label="Hardware Interface") >> pub_sub
    teleop >> Edge(label="Joystick Control") >> pub_sub
    training >> Edge(label="AR Tag Tracking") >> pub_sub
    sensors >> Edge(label="LaserScan Processing") >> pub_sub

    driver << Edge(label="Config Management") >> param_server
    teleop << Edge(label="Navigation Config") >> param_server

    nav_stack = Custom("Navigation Stack", "./icons/navigation.png")
    teleop >> Edge(label="Path Planning") >> nav_stack
    nav_stack >> Edge(label="Autonomous Navigation") >> driver

    tf_library = Custom("TF Library", "./icons/transform.png")
    tf_library << Edge(label="Coordinate Transformations") >> sensors

    pipeline = Custom("Data Processing Pipeline", "./icons/pipeline.png")
    sensors >> Edge(label="Sensor Data Processing") >> pipeline