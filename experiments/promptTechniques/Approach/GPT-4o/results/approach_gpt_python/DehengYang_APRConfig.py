from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.client import Client

with Diagram("Software Architecture Overview", show=False, direction="TB"):
    # Define clusters for modular components
    with Cluster("APRConfig"):
        dataset = Custom("Dataset", "./icons/dataset.png")
        localizer = Custom("Localizer", "./icons/localizer.png")
        apr_tools = Custom("APR Tools", "./icons/apr_tools.png")

    with Cluster("Traccar"):
        protocol_decoders = Custom("Protocol Decoders", "./icons/decoder.png")
        event_handlers = Custom("Event Handlers", "./icons/event_handler.png")
        geofencing = Custom("Geofencing", "./icons/geofence.png")

    with Cluster("JFreeChart"):
        chart_renderer = Custom("3D Pie Chart Renderer", "./icons/chart.png")

    with Cluster("Apache Commons"):
        math_utils = Custom("Math Utilities", "./icons/math.png")
        lang_utils = Custom("Lang Utilities", "./icons/lang.png")

    with Cluster("Google Closure Compiler"):
        js_compiler = Custom("JavaScript Compiler", "./icons/compiler.png")

    defects4j = Custom("Defects4J Benchmark", "./icons/benchmark.png")
    client = Client("User Interface")
    server = Server("Application Server")
    db = PostgreSQL("Database")

    # Define connections
    client >> Edge(label="requests") >> server
    server >> Edge(label="queries") >> db
    server >> Edge(label="fetches") >> defects4j

    server >> Edge(label="uses") >> dataset
    server >> Edge(label="uses") >> localizer
    server >> Edge(label="uses") >> apr_tools

    server >> Edge(label="integrates") >> protocol_decoders
    server >> Edge(label="integrates") >> event_handlers
    server >> Edge(label="integrates") >> geofencing

    server >> Edge(label="renders") >> chart_renderer
    server >> Edge(label="utilizes") >> math_utils
    server >> Edge(label="utilizes") >> lang_utils
    server >> Edge(label="compiles") >> js_compiler