from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.vcs import Git
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.blank import Blank

with Diagram("Linux Command Tutorial Repository Architecture", show=False, direction="TB"):
    with Cluster("Documentation Layer"):
        readme = LinuxGeneral("README.md")
        config = Server("_config.yml")
        
        with Cluster("Tutorial Modules"):
            basic_commands = LinuxGeneral("Basic Commands")
            filter_commands = LinuxGeneral("Filter Commands")
            file_permissions = LinuxGeneral("File Permissions")
            process_management = LinuxGeneral("Process Management")
            user_admin = LinuxGeneral("User Administration")
            group_admin = LinuxGeneral("Group Administration")
            editors = LinuxGeneral("Command Line Editors")
    
    with Cluster("Content Delivery"):
        nginx = Nginx("Nginx")
    
    with Cluster("Version Control"):
        git = Git("Git")
    
    readme >> [basic_commands, filter_commands, file_permissions, process_management, user_admin, group_admin, editors]
    config >> nginx
    git >> [readme, config, basic_commands, filter_commands, file_permissions, process_management, user_admin, group_admin, editors]