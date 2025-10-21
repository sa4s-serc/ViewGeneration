from diagrams import Diagram, Cluster, Edge
from diagrams.generic.device import Mobile
from diagrams.generic.blank import Blank
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet

with Diagram("NodleCode_n1 Architecture", show=False, direction="TB"):
    with Cluster("Device Tier"):
        ibeacon_device = Mobile("Dialog DA14531\n(iBeacon Device)")

    with Cluster("Application Tier"):
        mobile_app = Mobile("Nodle Mobile App")

    with Cluster("Data Tier"):
        cloud_backend = Server("Nodle Cloud")

    ibeacon_device >> Edge(label="BLE Advertising\n(UUID, Major, Minor)", style="dashed") >> mobile_app
    mobile_app >> Edge(label="Relay Beacon Info\n(Location, Attributes)", color="blue") >> cloud_backend
    mobile_app << Edge(label="Retrieve Beacon Data\n(API)", color="green") << cloud_backend

    with Cluster("PCB Manufacturing"):
        hardware_files = Internet("Hardware Design Files\n(Gerber, CNC)")

    ibeacon_device - Edge(label="PCB Design\n(Efficiency, Panelization)", style="dotted") - hardware_files