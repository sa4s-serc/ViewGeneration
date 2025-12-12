from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Internet
from diagrams.onprem.vcs import Git
from diagrams.onprem.iac import Ansible
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.storage import Ceph

with Diagram("System Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        with Cluster("Load Balancer"):
            lb1 = Server("LB 1")
            lb2 = Server("LB 2")
        
        with Cluster("Web Servers"):
            web1 = Server("Web 1")
            web2 = Server("Web 2")
            web3 = Server("Web 3")
    
    with Cluster("Application Layer"):
        with Cluster("App Servers"):
            app1 = Server("App 1")
            app2 = Server("App 2")
            app3 = Server("App 3")
        
        with Cluster("Microservices"):
            svc1 = Docker("Service A")
            svc2 = Docker("Service B")
            svc3 = Docker("Service C")
    
    with Cluster("Data Layer"):
        with Cluster("Database Cluster"):
            db_master = PostgreSQL("Master")
            db_slave1 = PostgreSQL("Slave 1")
            db_slave2 = PostgreSQL("Slave 2")
        
        with Cluster("Cache Layer"):
            cache1 = Redis("Redis 1")
            cache2 = Redis("Redis 2")
        
        with Cluster("Message Queue"):
            kafka1 = Kafka("Kafka 1")
            kafka2 = Kafka("Kafka 2")
        
        with Cluster("Storage"):
            storage = Ceph("Ceph Storage")
    
    with Cluster("Monitoring"):
        prom = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
    
    with Cluster("CI/CD"):
        git = Git("Git Repository")
        ansible = Ansible("Ansible")
    
    internet = Internet("Internet")
    
    # Connections
    user >> internet >> lb1
    user >> internet >> lb2
    lb1 >> web1
    lb1 >> web2
    lb2 >> web2
    lb2 >> web3
    
    web1 >> app1
    web2 >> app2
    web3 >> app3
    
    app1 >> svc1
    app2 >> svc2
    app3 >> svc3
    
    svc1 >> db_master
    svc2 >> db_slave1
    svc3 >> db_slave2
    svc1 >> cache1
    svc2 >> cache2
    svc3 >> kafka1
    svc1 >> kafka2
    svc2 >> storage
    svc3 >> storage
    
    db_master >> db_slave1
    db_master >> db_slave2
    
    # Monitoring connections
    web1 >> prom
    web2 >> prom
    web3 >> prom
    app1 >> prom
    app2 >> prom
    app3 >> prom
    svc1 >> prom
    svc2 >> prom
    svc3 >> prom
    db_master >> prom
    cache1 >> prom
    kafka1 >> prom
    prom >> grafana
    
    # CI/CD connections
    git >> ansible
    ansible >> web1
    ansible >> web2
    ansible >> web3
    ansible >> app1
    ansible >> app2
    ansible >> app3