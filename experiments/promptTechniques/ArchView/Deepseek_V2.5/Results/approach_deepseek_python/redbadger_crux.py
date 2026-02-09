from diagrams import Diagram, Cluster
from diagrams.generic.device import Mobile
from diagrams.generic.os import Android, IOS
from diagrams.programming.language import Rust, Swift, Kotlin, TypeScript
from diagrams.onprem.client import Client
from diagrams.aws.general import User
from diagrams.generic.blank import Blank

with Diagram("Crux Cross-Platform Architecture", show=False, direction="TB"):
    with Cluster("Rust Core (Shared Business Logic)"):
        app_trait = Blank("App Trait\n(Events, Model, ViewModel)")
        core_struct = Blank("Core Struct\n(State Management)")
        effect_trait = Blank("Effect Trait\n(Side Effects)")
        capabilities = Blank("Capabilities\n(HTTP, Time, KV Store)")
        command_pattern = Blank("Command Pattern\n(RequestBuilder)")
        
        app_trait >> core_struct
        core_struct >> effect_trait
        core_struct >> capabilities
        capabilities >> command_pattern
    
    bridge = Blank("Bridge\n(FFI Communication)")
    
    with Cluster("Platform Shells"):
        with Cluster("iOS"):
            ios_shell = Swift("iOS Shell")
            ios_user = IOS("iOS User")
            ios_shell >> ios_user
        
        with Cluster("Android"):
            android_shell = Kotlin("Android Shell")
            android_user = Android("Android User")
            android_shell >> android_user
        
        with Cluster("Web"):
            web_shell = TypeScript("Web Shell")
            web_user = Client("Web User")
            web_shell >> web_user
    
    core_struct >> bridge
    bridge >> ios_shell
    bridge >> android_shell
    bridge >> web_shell
    
    with Cluster("Architectural Patterns"):
        mvu_pattern = Blank("MVU Pattern\n(Model-View-Update)")
        ports_adapters = Blank("Ports & Adapters\n(Hexagonal)")
    
    core_struct - mvu_pattern
    core_struct - ports_adapters