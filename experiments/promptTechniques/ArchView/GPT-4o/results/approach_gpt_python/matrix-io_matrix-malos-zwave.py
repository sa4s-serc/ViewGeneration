from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.programming.flowchart import Action, Decision

with Diagram("Matrix-IO MALOS Z-Wave Architecture", show=False):
    # Define custom nodes
    matrix_creator = Custom("MATRIX Creator/Voice", "./icons/matrix_creator.png")
    zip_gateway = Custom("Z/IP Gateway", "./icons/zip_gateway.png")
    zmq = Custom("0MQ", "./icons/zmq.png")
    protocol_buffers = Custom("Protocol Buffers", "./icons/protocol_buffers.png")

    # Define main components
    with Cluster("MALOS Integration"):
        malos = Custom("MALOS Core", "./icons/malos.png")

    with Cluster("Z-Wave Abstraction Layer"):
        command_classes = [
            Custom("COMMAND_CLASS_SWITCH_BINARY", "./icons/command_class.png"),
            Custom("COMMAND_CLASS_SENSOR_MULTILEVEL", "./icons/command_class.png"),
            Custom("COMMAND_CLASS_SCHEDULE", "./icons/command_class.png"),
            Custom("COMMAND_CLASS_SECURITY", "./icons/command_class.png"),
            Custom("COMMAND_CLASS_SCREEN", "./icons/command_class.png"),
        ]

    # Interactions
    matrix_creator >> Edge(label="serial communication") >> zip_gateway
    zip_gateway >> Edge(label="Z-Wave RF protocol") >> command_classes[0]

    malos >> Edge(label="abstracts hardware") >> command_classes[1]
    malos >> Edge(label="abstracts hardware") >> command_classes[2]

    command_classes[3] >> Edge(label="secure communication") >> matrix_creator
    command_classes[4] >> Edge(label="display info") >> matrix_creator

    # Communication through 0MQ and Protocol Buffers
    malos >> Edge(label="message queue") >> zmq
    zmq >> Edge(label="data serialization") >> protocol_buffers

    # JavaScript utilities
    js_utilities = [
        Action("addnode.js"),
        Action("list.js"),
        Action("removenode.js"),
        Action("simpleTest.js"),
        Action("test_zwave_accel.js"),
    ]

    for util in js_utilities:
        util >> Edge(label="uses") >> zmq

    # Service architecture
    service_script = Decision("matrixio-malos-zwave.service")
    service_script >> Edge(label="starts") >> malos