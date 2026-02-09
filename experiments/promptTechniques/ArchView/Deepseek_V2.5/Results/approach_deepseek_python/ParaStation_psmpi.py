from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Ansible
from diagrams.onprem.logging import Fluentbit
from diagrams.onprem.network import Apache

with Diagram("ParaStation MPI (PSMPI) Layered Architecture", show=False, direction="TB"):
    with Cluster("MPI Standard Implementation"):
        mpi_interface = Server("MPI Interface")
    
    with Cluster("Communication Layer"):
        pscom = Server("PSCOM")
        shared_memory = Server("Shared Memory")
        rdma = Server("RDMA")
        tcp = Server("TCP")
    
    with Cluster("Process Management"):
        hydra = Server("Hydra PM")
        psmgmt = Server("PSMGMT")
        pmix = Server("PMIx")
    
    with Cluster("Collectives Framework"):
        ucg = Server("UCG")
        hcoll = Server("HCOLL")
    
    with Cluster("Data Handling"):
        yaksa = Server("Yaksa")
        romio = Server("ROMIO")
    
    with Cluster("Hardware Integration"):
        hwloc = Server("HWLOC")
        cuda = Server("CUDA")
        ucx = Server("UCX")
    
    with Cluster("Build & Configuration"):
        autotools = Server("Autotools")
        configure = Server("Configure")
        cvars = Server("CVARs")
    
    with Cluster("Testing & Monitoring"):
        test_suite = Server("MPICH Test Suite")
        jenkins = Jenkins("Jenkins CI")
        prometheus = Prometheus("Monitoring")
        grafana = Grafana("Dashboards")
        fluentbit = Fluentbit("Logging")

    mpi_interface >> pscom
    pscom >> [shared_memory, rdma, tcp]
    mpi_interface >> [hydra, psmgmt, pmix]
    mpi_interface >> ucg
    ucg >> hcoll
    mpi_interface >> yaksa
    mpi_interface >> romio
    mpi_interface >> hwloc
    hwloc >> cuda
    pscom >> ucx
    autotools >> configure
    configure >> cvars
    test_suite >> jenkins
    [mpi_interface, pscom, ucg, yaksa, romio] >> fluentbit
    fluentbit >> prometheus
    prometheus >> grafana