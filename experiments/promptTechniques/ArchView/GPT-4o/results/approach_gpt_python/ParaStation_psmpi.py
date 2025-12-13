from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.onprem.client import Client
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import Kafka
from diagrams.onprem.iac import Ansible
from diagrams.onprem.vcs import Git
from diagrams.onprem.ci import Jenkins
from diagrams.programming.language import Python
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.storage import Ceph
from diagrams.onprem.compute import Nomad

with Diagram("ParaStation MPI (PSMPI) Architecture", show=False, direction="TB"):

    with Cluster("Communication Subsystem"):
        pscom = Kafka("pscom")
        rdma = Server("RDMA")
        shared_mem = Ceph("Shared Memory")

    with Cluster("Process Management"):
        hydra = Docker("Hydra")
        psmgmt = Docker("ParaStation Management")

    with Cluster("Networking Module"):
        tcp = Internet("TCP")

    with Cluster("Data Transport Technologies"):
        ib = Server("InfiniBand")
    
    with Cluster("Build System"):
        autotools = Ansible("Autotools")
        configure = Python("Configure Script")

    with Cluster("Key Components and Libraries"):
        pscm = Server("PSCOM")
        hcoll = Server("HCOLL")
        hwloc = Server("HWLOC")
        romio = Server("ROMIO")
        yaksa = Server("Yaksa")

    with Cluster("Testing Infrastructure"):
        test_suite = Git("MPICH Test Suite")
        ci_cd = Jenkins("Jenkins CI/CD")

    with Cluster("Performance Optimizations"):
        dma = Nomad("DMA")
        zero_copy = Prometheus("Zero Copy")
        
    mpi = Client("MPI Standard Implementation")
    
    mpi >> Edge(label="implements") >> pscom
    mpi >> Edge(label="builds on") >> pscm
    mpi >> Edge(label="supports") >> hydra
    mpi >> Edge(label="supports") >> psmgmt
    mpi >> Edge(label="uses") >> tcp
    mpi >> Edge(label="utilizes") >> ib
    mpi >> Edge(label="configured by") >> autotools
    mpi >> Edge(label="configured by") >> configure
    mpi >> Edge(label="leverages") >> shared_mem
    mpi >> Edge(label="leverages") >> rdma
    mpi >> Edge(label="integrates") >> hcoll
    mpi >> Edge(label="integrates") >> hwloc
    mpi >> Edge(label="integrates") >> romio
    mpi >> Edge(label="uses") >> yaksa
    mpi >> Edge(label="validated by") >> test_suite
    mpi >> Edge(label="integrated with") >> ci_cd
    mpi >> Edge(label="optimized by") >> dma
    mpi >> Edge(label="optimized by") >> zero_copy