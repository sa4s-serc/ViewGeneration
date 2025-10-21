from diagrams import Diagram, Cluster, Edge
from diagrams.generic.blank import Blank
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.storage import LocalStorage

with Diagram("ARGAEL Architecture", show=False, direction="TB"):

    user = User("User")

    with Cluster("ARGAEL Application"):
        gui = Server("ArgaelForm.java")
        io_manager = Server("IOManager.java")
        data_manager = Server("DataManager.java")
        report_formatter = Server("ReportFormatter.java")
        init_params = Server("InitParams.java")
        file_utils = Server("FileUtils.java")
        string_utils = Server("StringUtils.java")
        argument_model = Server("ArgumentModel.java")
        selected_items = Server("SelectedItems.java")

    with Cluster("Data Storage"):
        jsonl_storage = LocalStorage("JSONL Files")
        csv_storage = LocalStorage("CSV Files")

    with Cluster("Configuration"):
        params_json = LocalStorage("params.json")
        users_txt = LocalStorage("users.txt")
        html_templates = LocalStorage("HTML Templates")

    user >> gui
    gui >> Edge(label="reads/writes") >> io_manager
    io_manager >> Edge(label="manages") >> data_manager
    data_manager >> Edge(label="formats") >> report_formatter
    report_formatter >> Edge(label="uses") >> html_templates

    init_params >> Edge(label="configures") >> params_json
    gui >> Edge(label="views") >> jsonl_storage
    gui >> Edge(label="exports") >> csv_storage

    io_manager >> file_utils
    io_manager >> string_utils
    io_manager >> argument_model
    gui >> selected_items

    users_txt << Edge(label="manages") << data_manager