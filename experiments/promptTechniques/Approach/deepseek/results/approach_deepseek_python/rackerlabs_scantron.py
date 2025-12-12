from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.compute import Server
from diagrams.onprem.storage import Ceph
from diagrams.onprem.iac import Ansible
from diagrams.programming.framework import Django
from diagrams.onprem.network import Internet

with Diagram("Scantron Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Web Frontend"):
        nginx = Nginx("Nginx")
        django_app = Django("Django Console")
    
    with Cluster("Database Layer"):
        db = PostgreSQL("PostgreSQL")
        redis = Redis("Redis Queue")
    
    with Cluster("Scanning Engines"):
        engine1 = Server("Engine 1")
        engine2 = Server("Engine 2")
        engine3 = Server("Engine 3")
    
    with Cluster("Shared Storage"):
        nfs = Ceph("NFS Share")
    
    with Cluster("Automation"):
        ansible = Ansible("Ansible")
    
    internet = Internet("Target Networks")
    
    user >> nginx >> django_app
    django_app >> db
    django_app >> redis
    django_app >> [engine1, engine2, engine3]
    [engine1, engine2, engine3] >> nfs
    [engine1, engine2, engine3] >> internet
    ansible >> [django_app, engine1, engine2, engine3]