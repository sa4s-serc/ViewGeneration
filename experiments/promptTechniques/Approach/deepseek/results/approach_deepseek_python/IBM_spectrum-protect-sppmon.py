from diagrams import Diagram, Cluster
from diagrams.onprem.database import InfluxDB
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Apache
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import PostgreSQL

with Diagram("SPPMon Architecture", show=False):
    user = User("User")
    
    with Cluster("SPPMon Core"):
        sppmon_core = Server("SPPMon Core Engine")
        rest_client = Apache("REST API Client")
        ssh_client = Server("SSH Client")
        
    with Cluster("Data Collection"):
        spp_server = Server("SPP Server")
        vsnap = Server("vSnap")
        vadp = Server("VADP")
        m365_proxy = Server("M365 Proxy")
    
    with Cluster("Data Processing"):
        influx = InfluxDB("InfluxDB")
        grafana = Grafana("Grafana")
    
    with Cluster("SPPCheck"):
        sppcheck = Server("SPPCheck")
        excel_processor = Server("Excel Processor")
        predictor = Server("Predictor")
        report_generator = Server("Report Generator")
    
    with Cluster("Automation"):
        installer = Server("Installer Script")
        config_generator = Server("Config Generator")
        cron_manager = Server("Cron Manager")
    
    user >> grafana
    sppmon_core >> rest_client >> spp_server
    sppmon_core >> ssh_client >> [vsnap, vadp, m365_proxy]
    sppmon_core >> influx
    influx >> grafana
    sppcheck >> [excel_processor, predictor, report_generator]
    installer >> [config_generator, cron_manager]