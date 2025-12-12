from diagrams import Diagram, Cluster
from diagrams.programming.framework import Spring, React
from diagrams.programming.language import Java
from diagrams.onprem.database import MySQL
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.container import Docker

with Diagram("ZWT Framework Architecture", show=False):
    with Cluster("ZWT Framework"):
        with Cluster("Core Layer"):
            core = Java("Core Abstraction")
            
        with Cluster("UI Components"):
            components = [
                Spring("ZwtComponent"),
                Spring("ZwtContainer"),
                Spring("ZwtFrame"),
                Spring("ZwtPanel")
            ]
            core - components

        with Cluster("Platform-Specific Implementations"):
            implementations = [
                Docker("Java SE/EE"),
                Docker("Java ME"),
                Docker("Android")
            ]
            
            for impl in implementations:
                core >> impl

        with Cluster("Services"):
            graphics = Spring("ZwtGraphics")
            keyboard = Spring("ZwtKeyboard")
            events = Spring("Event Handling")
            layout = Spring("Layout Management")

            core >> graphics
            core >> keyboard
            core >> events
            core >> layout

        with Cluster("Storage"):
            db = MySQL("Component State")
            core >> db

        with Cluster("Event Bus"):
            queue = RabbitMQ("Event Queue")
            events >> queue

        with Cluster("Frontend"):
            ui = React("UI Layer")
            components >> ui