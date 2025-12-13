from diagrams import Diagram, Cluster
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.storage import Ceph
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.monitoring import Grafana, Prometheus

with Diagram("Rinkako_CStoreDBMS Architecture", show=False, direction="TB"):
    with Cluster("DBInterface Layer"):
        db_controller = Server("DBController")
        connection_pool = Server("DBConnectionPool")
    
    with Cluster("DBCompiler Layer"):
        lexical_analyzer = Server("LexicalAnalyzer")
        syntax_parser = Server("SyntaxParser")
        pile = Server("Pile")
        db_bridge = Server("DBBridge")
        cs_database = Server("CSDatabase")
    
    with Cluster("DBEngine Layer"):
        file_manager = Server("FileManager")
        table_manager = Server("TableManager")
        db_allocator = Server("DBAllocator")
        db_lock = Server("DBLock")
        db_transaction = Server("DBTransaction")
    
    db_controller >> connection_pool
    connection_pool >> db_bridge
    db_bridge >> lexical_analyzer
    db_bridge >> syntax_parser
    db_bridge >> pile
    db_bridge >> cs_database
    cs_database >> file_manager
    cs_database >> table_manager
    cs_database >> db_allocator
    cs_database >> db_lock
    cs_database >> db_transaction