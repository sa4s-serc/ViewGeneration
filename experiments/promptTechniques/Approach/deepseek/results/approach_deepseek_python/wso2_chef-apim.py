from diagrams import Diagram
from diagrams.onprem.iac import Ansible
from diagrams.onprem.database import MySQL
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Apache
from diagrams.programming.language import Java

with Diagram("WSO2 API Manager 2.2.0 Chef Cookbook Architecture", show=False, direction="TB"):
    user = User("User")
    
    chef_server = Ansible("Chef Server")
    
    java = Java("Java Runtime")
    
    wso2_components = [
        Server("Key Manager"),
        Server("Publisher"),
        Server("Store"),
        Server("Traffic Manager"),
        Server("Gateway Manager"),
        Server("Gateway Worker")
    ]
    
    mysql_db = MySQL("MySQL Database")
    redis_cache = Redis("Redis Cache")
    apache_lb = Apache("Apache Load Balancer")
    
    user >> chef_server
    
    chef_server >> java
    java >> wso2_components
    
    for component in wso2_components:
        component >> mysql_db
        component >> redis_cache
    
    apache_lb >> wso2_components[-2:]
    
    wso2_components[-2:] >> apache_lb