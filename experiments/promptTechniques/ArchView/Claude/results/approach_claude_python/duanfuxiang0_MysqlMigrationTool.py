from diagrams import Diagram
from diagrams.programming.language import Go
from diagrams.onprem.database import MySQL
from diagrams.generic.database import SQL
from diagrams.programming.flowchart import Document

with Diagram("Incremental Data Migration Architecture", show=False, direction="TB"):
    # Data Sources
    mysql = MySQL("Source MySQL")
    binlog = Document("Binlog Stream")
    
    # Core Components
    canal = Go("go-mysql/canal")
    parser = Go("BinlogParser")
    handler = Go("RowEventHandler")
    mapper = Go("Reflection Mapper")
    
    # Target
    dest_db = SQL("Destination DB")
    
    # Data Models
    models = Document("Data Models\n(User, Email, Mobile)")

    # Flow
    mysql >> binlog >> canal >> parser
    parser >> handler >> mapper
    mapper >> models >> dest_db
    
    # Add descriptions
    canal - Document("Captures & parses\nbinlog events")
    parser - Document("Converts MySQL\ntypes to Go types") 
    handler - Document("Processes row events\n& handles errors")
    mapper - Document("Maps data using\nstruct reflection")