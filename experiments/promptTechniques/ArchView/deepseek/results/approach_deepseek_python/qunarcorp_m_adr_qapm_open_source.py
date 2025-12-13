from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.generic.device import Mobile
from diagrams.generic.blank import Blank
from diagrams.programming.language import Java
from diagrams.onprem.database import Database
from diagrams.onprem.network import Internet
from diagrams.onprem.ci import Jenkins

with Diagram("QAPM Android APM Library Architecture", show=False, direction="TB"):
    user = User("Android User")
    android_app = Mobile("Android Application")
    
    with Cluster("Build Process"):
        gradle_plugin = Jenkins("QAPM Gradle Plugin")
        aop_transform = Blank("AspectJ Transform")
        gradle_plugin >> aop_transform
    
    with Cluster("QAPM Library"):
        qapm_core = Java("QAPM.java\n(Entry Point)")
        
        with Cluster("Monitoring Components"):
            config_mgr = Blank("QConfigManager")
            watchman = Blank("WatchMan")
            
            with Cluster("Tracers"):
                network_tracer = Blank("Network Tracer")
                fps_tracer = Blank("FPS Tracer")
                memory_tracer = Blank("Memory Tracer")
                cpu_tracer = Blank("CPU Tracer")
                battery_tracer = Blank("Battery Tracer")
            
            with Cluster("Data Management"):
                storage = Database("Storage")
                network_sender = Blank("Network Sender")
        
        qapm_core >> config_mgr
        qapm_core >> watchman
        watchman >> [network_tracer, fps_tracer, memory_tracer, cpu_tracer, battery_tracer]
        [network_tracer, fps_tracer, memory_tracer, cpu_tracer, battery_tracer] >> storage
        storage >> network_sender
    
    external_endpoint = Internet("External Endpoint")
    
    android_app >> gradle_plugin
    aop_transform >> qapm_core
    android_app - qapm_core
    network_sender >> external_endpoint