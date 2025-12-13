from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet, Nginx
from diagrams.onprem.compute import Nomad
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.analytics import Spark
from diagrams.onprem.network import Istio

with Diagram("ParaStation MPI Architecture", show=False, direction="TB"):
    
    internet = Internet("External Network")
    
    with Cluster("Process Management"):
        pmix = Nomad("PMIx")
        psmgmt = Server("PSMgmt")
        
    with Cluster("Communication Layer"):
        pscom = Server("PSCOM")
        pipeline = Istio("Message Pipelining") 
        tcp = Nginx("TCP Transport")
        
    with Cluster("Data Transport"):
        rdma = Server("RDMA")
        infiniband = Server("InfiniBand")
        shm = Server("Shared Memory")
        
    with Cluster("Performance & Monitoring"):
        monitor = Prometheus("Monitoring")
        perf = Spark("Performance Analysis")

    # Connect components
    internet >> pmix
    internet >> psmgmt
    
    pmix >> pscom
    psmgmt >> pscom
    
    pscom >> pipeline
    pipeline >> tcp
    
    tcp >> rdma
    tcp >> infiniband 
    tcp >> shm
    
    rdma >> monitor
    infiniband >> monitor
    shm >> monitor
    
    monitor >> perf