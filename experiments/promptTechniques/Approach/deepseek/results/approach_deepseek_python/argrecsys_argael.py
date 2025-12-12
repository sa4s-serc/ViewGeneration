from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.language import Java
from diagrams.onprem.database import MongoDB
from diagrams.onprem.storage import Ceph
from diagrams.onprem.network import Nginx
from diagrams.onprem.workflow import Airflow

with Diagram("ARGAEL Architecture View", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("GUI Layer"):
        gui = Java("ArgaelForm")
    
    with Cluster("Data Management Layer"):
        data_manager = Java("DataManager")
        argument_model = Java("ArgumentModel")
        tree_node = Java("TreeNode")
        selected_items = Java("SelectedItems")
    
    with Cluster("IO Layer"):
        io_manager = Java("IOManager")
        file_utils = Java("FileUtils")
        string_utils = Java("StringUtils")
        report_formatter = Java("ReportFormatter")
        init_params = Java("InitParams")
    
    with Cluster("Configuration"):
        params = Ceph("params.json")
        users = Ceph("users.txt")
    
    with Cluster("Data Storage"):
        proposals = MongoDB("Proposals")
        comments = MongoDB("Comments")
    
    with Cluster("Templates"):
        html_templates = Nginx("HTML Templates")
    
    user >> gui
    gui >> data_manager
    gui >> io_manager
    data_manager >> argument_model
    data_manager >> tree_node
    data_manager >> selected_items
    io_manager >> file_utils
    io_manager >> string_utils
    io_manager >> report_formatter
    io_manager >> init_params
    init_params >> params
    data_manager >> users
    data_manager >> proposals
    data_manager >> comments
    report_formatter >> html_templates