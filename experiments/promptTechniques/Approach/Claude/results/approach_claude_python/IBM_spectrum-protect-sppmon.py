from diagrams import Diagram, Cluster
from diagrams.onprem.database import InfluxDB
from diagrams.onprem.monitoring import Grafana
from diagrams.programming.language import Python
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.generic.storage import Storage

with Diagram("SPPMon Architecture", show=False, direction="LR"):
    with Cluster("Data Collection"):
        spp = Server("SPP Server")
        vsnap = Server("vSnap")
        vadp = Server("VADP")
        m365 = Server("M365 Proxies")
        collector = Python("SPPMon Core")
        
        spp >> collector
        vsnap >> collector
        vadp >> collector
        m365 >> collector

    with Cluster("Data Processing & Storage"):
        influx = InfluxDB("InfluxDB")
        collector >> influx

    with Cluster("Visualization & Analysis"):
        grafana = Grafana("Grafana")
        influx >> grafana

    with Cluster("SPPCheck"):
        sppcheck = Python("SPPCheck")
        reports = Storage("PDF Reports")
        
        influx >> sppcheck
        sppcheck >> reports