from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.storage import Ceph
from diagrams.programming.language import Cpp, C
from diagrams.generic.network import Firewall

graph_attr = {
    "fontsize": "20",
    "bgcolor": "white"
}

with Diagram("Pollard's Kangaroo ECDLP Solver Architecture", show=False, direction="TB", graph_attr=graph_attr):
    
    with Cluster("Client Layer"):
        client = Server("Client")
    
    with Cluster("Server Layer"):
        server = Server("Server")
        
        with Cluster("Core Components"):
            kangaroo = Cpp("Kangaroo")
            secp256k1 = Cpp("Secp256K1")
            gpu_engine = Cpp("GPUEngine")
            hash_table = Cpp("HashTable")
            network = Cpp("Network")
            backup = Cpp("Backup")
            thread_mgmt = Cpp("Thread")
            timer = Cpp("Timer")
        
        with Cluster("Supporting Components"):
            integer_arithmetic = Cpp("Int Arithmetic")
            constants = Cpp("Constants")
            merge = Cpp("Merge")
            part_merge = Cpp("PartMerge")
            check = Cpp("Check")
    
    with Cluster("Storage Layer"):
        work_files = Ceph("Work Files")
        hash_table_storage = MongoDB("Hash Table Data")
    
    with Cluster("Hardware Layer"):
        cpu = Server("CPU")
        gpu = Server("GPU")
    
    # Connections
    client >> server
    server >> kangaroo
    kangaroo >> secp256k1
    kangaroo >> gpu_engine
    kangaroo >> hash_table
    kangaroo >> network
    kangaroo >> backup
    kangaroo >> thread_mgmt
    kangaroo >> timer
    
    secp256k1 >> integer_arithmetic
    gpu_engine >> gpu
    thread_mgmt >> cpu
    
    kangaroo >> work_files
    hash_table >> hash_table_storage
    
    kangaroo >> constants
    kangaroo >> merge
    kangaroo >> part_merge
    kangaroo >> check