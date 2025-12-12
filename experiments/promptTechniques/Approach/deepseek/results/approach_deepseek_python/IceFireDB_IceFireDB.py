from diagrams import Diagram, Cluster
from diagrams.onprem.database import Redis, MySQL
from diagrams.onprem.network import Envoy
from diagrams.onprem.queue import Kafka
from diagrams.onprem.inmemory import Memcached
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.programming.language import Go
from diagrams.generic.network import Switch
from diagrams.generic.storage import Storage
from diagrams.generic.database import SQL
from diagrams.aws.database import RDS
from diagrams.aws.network import CloudFront
from diagrams.aws.compute import EC2

with Diagram("IceFireDB Architecture", show=False, direction="TB"):
    with Cluster("Core Database Layer"):
        leveldb = Storage("LevelDB Storage")
        redis_protocol = Redis("Redis Protocol")
        raft_consensus = Server("Raft Consensus\n(uhaha)")
        core_db = [leveldb, redis_protocol, raft_consensus]
    
    with Cluster("SQL Proxy Layer"):
        mysql_proxy = MySQL("MySQL Proxy")
        p2p_network = Switch("P2P Network\n(libp2p)")
        connection_pool = Docker("Connection Pool")
        sql_proxy = [mysql_proxy, p2p_network, connection_pool]
    
    with Cluster("Storage Engines"):
        leveldb_engine = Storage("LevelDB")
        crdt_engine = Memcached("CRDT")
        ipfs_engine = Storage("IPFS")
        oss_engine = Storage("OSS")
        hybrid_engine = SQL("HybridDB")
        storage_engines = [leveldb_engine, crdt_engine, ipfs_engine, oss_engine, hybrid_engine]
    
    with Cluster("Communication Layer"):
        grpc_server = Server("gRPC Server")
        grpc_client = Server("gRPC Client")
        http2_transport = Envoy("HTTP/2 Transport")
        communication = [grpc_server, grpc_client, http2_transport]
    
    with Cluster("Security Layer"):
        crypto_lib = Go("Crypto Library")
        key_management = Server("Key Management")
        security = [crypto_lib, key_management]
    
    with Cluster("Monitoring & Observability"):
        opentelemetry = Server("OpenTelemetry")
        metrics = Kafka("Metrics Collection")
        monitoring = [opentelemetry, metrics]
    
    redis_protocol >> leveldb
    raft_consensus >> redis_protocol
    mysql_proxy >> p2p_network
    connection_pool >> mysql_proxy
    p2p_network >> storage_engines
    grpc_server >> grpc_client
    http2_transport >> grpc_server
    crypto_lib >> key_management
    opentelemetry >> metrics
    redis_protocol >> mysql_proxy
    mysql_proxy >> grpc_server
    grpc_client >> crypto_lib
    key_management >> opentelemetry