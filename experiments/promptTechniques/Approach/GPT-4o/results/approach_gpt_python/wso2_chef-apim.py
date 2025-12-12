from diagrams import Diagram, Cluster, Node
from diagrams.generic.os import Centos
from diagrams.onprem.database import MySQL
from diagrams.custom import Custom

with Diagram("WSO2 API Manager Architecture", show=False, direction="TB"):
    client = Custom("Client", "./client-icon.png")

    with Cluster("WSO2 API Manager Deployment"):
        with Cluster("WSO2 API Manager Profiles"):
            key_manager = Custom("Key Manager", "./key-manager-icon.png")
            publisher = Custom("Publisher", "./publisher-icon.png")
            store = Custom("Store", "./store-icon.png")
            traffic_manager = Custom("Traffic Manager", "./traffic-manager-icon.png")
            gateway_manager = Custom("Gateway Manager", "./gateway-manager-icon.png")
            gateway_worker = Custom("Gateway Worker", "./gateway-worker-icon.png")

        with Cluster("Java Environment"):
            java = Custom("Java", "./java-icon.png")

        with Cluster("Configuration Management"):
            carbon = Custom("carbon.xml", "./config-icon.png")
            axis2 = Custom("axis2.xml", "./config-icon.png")
            datasources = Custom("master-datasources.xml", "./config-icon.png")

        client >> key_manager
        client >> publisher
        client >> store
        client >> traffic_manager
        client >> gateway_manager
        client >> gateway_worker

        key_manager >> carbon
        publisher >> axis2
        store >> datasources

        gateway_manager >> java
        gateway_worker >> java

    with Cluster("Database"):
        mysql = MySQL("MySQL Database")
        
    gateway_manager >> mysql
    gateway_worker >> mysql