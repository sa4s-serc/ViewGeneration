from diagrams import Diagram
from diagrams.onprem.database import MySQL
from diagrams.onprem.database import Postgresql
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker

with Diagram("Incremental Data Migration Tool Architecture", show=False, direction="LR"):
    source_db = MySQL("Source MySQL")
    
    binlog_parser = Server("Binlog Parser")
    
    data_models = Docker("Data Models\n(User, Email, Mobile)")
    
    target_db = Postgresql("Target Database")
    
    source_db >> binlog_parser
    binlog_parser >> data_models
    data_models >> target_db