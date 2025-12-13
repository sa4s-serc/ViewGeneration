from diagrams import Diagram, Cluster, Node
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.database import Influxdb
from diagrams.onprem.compute import Server
from diagrams.onprem.client import User
from diagrams.onprem.container import Docker

with Diagram("SPPMon Architecture", show=False):
    user = User("Admin")

    with Cluster("SPPMon System"):
        sppmon_core = Server("SPPMon Core")
        sppcheck = Server("SPPCheck")

        with Cluster("Data Collection"):
            rest_client = Server("REST Client")
            ssh_client = Server("SSH Client")

        with Cluster("Data Storage & Processing"):
            influxdb = Influxdb("InfluxDB")

        with Cluster("Data Visualization"):
            grafana = Grafana("Grafana")

        user >> sppmon_core
        sppmon_core >> rest_client
        sppmon_core >> ssh_client
        rest_client >> influxdb
        ssh_client >> influxdb
        influxdb >> grafana
        user << grafana

    with Cluster("Automated Installation & Configuration"):
        installer_scripts = Server("Installer Scripts")
        sppmon_core << installer_scripts

    sppcheck << influxdb
    sppcheck >> Node("PDF Report Generation")