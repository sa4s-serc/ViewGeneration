from diagrams import Diagram, Cluster
from diagrams.onprem.database import MySQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Etcd
from diagrams.onprem.compute import Server
from diagrams.programming.language import Go
from diagrams.aws.storage import S3

with Diagram("Teamgram Server Architecture", show=False, direction="TB"):
    client = Server("Client")
    
    with Cluster("BFF Layer"):
        bff_messages = Go("BFF Messages")
        bff_privacy = Go("BFF Privacy")
    
    with Cluster("Core Services"):
        with Cluster("Message Services"):
            msg_service = Go("msg Service")
            kafka = Kafka("Kafka")
        
        with Cluster("Chat Services"):
            chat_service = Go("chat Service")
        
        with Cluster("User Services"):
            user_service = Go("user Service")
            redis_user = Redis("Redis Cache")
        
        with Cluster("Auth Services"):
            auth_service = Go("authsession Service")
            code_service = Go("code Service")
            redis_auth = Redis("Redis Cache")
        
        with Cluster("Media Services"):
            media_service = Go("media Service")
            dfs_service = Go("dfs Service")
            minio = S3("MinIO Storage")
        
        with Cluster("Other Services"):
            username_service = Go("username Service")
            dialog_service = Go("dialog Service")
            updates_service = Go("updates Service")
            idgen_service = Go("idgen Service")
    
    with Cluster("Data Layer"):
        mysql = MySQL("MySQL Database")
        etcd = Etcd("Service Discovery")
    
    client >> bff_messages
    client >> bff_privacy
    bff_messages >> msg_service
    bff_privacy >> user_service
    msg_service >> kafka
    msg_service >> chat_service
    msg_service >> user_service
    chat_service >> user_service
    user_service >> redis_user
    auth_service >> redis_auth
    code_service >> redis_auth
    media_service >> dfs_service
    dfs_service >> minio
    username_service >> user_service
    dialog_service >> updates_service
    idgen_service >> redis_user
    msg_service >> mysql
    chat_service >> mysql
    user_service >> mysql
    auth_service >> mysql
    code_service >> mysql
    media_service >> mysql
    username_service >> mysql
    dialog_service >> mysql
    updates_service >> mysql
    idgen_service >> mysql
    msg_service >> etcd
    chat_service >> etcd
    user_service >> etcd
    auth_service >> etcd
    code_service >> etcd
    media_service >> etcd
    username_service >> etcd
    dialog_service >> etcd
    updates_service >> etcd
    idgen_service >> etcd