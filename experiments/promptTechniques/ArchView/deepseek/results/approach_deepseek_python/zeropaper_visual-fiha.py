from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki
from diagrams.onprem.tracing import Jaeger
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.vcs import Git

with Diagram("Visual Fiha Architecture", show=False, direction="TB"):
    user = User("VS Code User")
    
    with Cluster("VS Code Extension"):
        vf_extension = Server("VFExtension")
        web_server = Server("WebServer")
        redux_store = Server("Redux Store")
        
        with Cluster("Commands"):
            commands = [Server("Command 1"), Server("Command 2")]
    
    with Cluster("WebViews"):
        audio_view = Server("AudioView")
        control_view = Server("ControlView")
        displays_view = Server("DisplaysView")
        timeline_view = Server("TimelineView")
    
    with Cluster("Display Workers"):
        display_worker = Server("DisplayWorker")
        script_runner = Server("ScriptRunner")
        scriptable = Server("Scriptable")
    
    with Cluster("Layers"):
        canvas_2d = Server("Canvas2DLayer")
        three_js = Server("ThreeJSLayer")
    
    with Cluster("Capture"):
        audio_capture = Server("AudioCapture")
        midi_capture = Server("MIDICapture")
    
    with Cluster("Communication"):
        com_module = Server("Com Module")
    
    with Cluster("Utilities"):
        math_tools = Server("MathTools")
        misc_tools = Server("MiscTools")
        asset_mgmt = Server("AssetMgmt")
    
    user >> vf_extension
    vf_extension >> web_server
    vf_extension >> redux_store
    vf_extension >> commands
    vf_extension >> com_module
    
    web_server >> audio_view
    web_server >> control_view
    web_server >> displays_view
    web_server >> timeline_view
    web_server >> audio_capture
    web_server >> midi_capture
    
    com_module >> display_worker
    display_worker >> script_runner
    script_runner >> scriptable
    script_runner >> canvas_2d
    script_runner >> three_js
    
    redux_store >> audio_view
    redux_store >> control_view
    redux_store >> displays_view
    redux_store >> timeline_view
    
    com_module >> audio_view
    com_module >> control_view
    com_module >> displays_view
    com_module >> timeline_view
    
    math_tools >> script_runner
    misc_tools >> script_runner
    asset_mgmt >> script_runner