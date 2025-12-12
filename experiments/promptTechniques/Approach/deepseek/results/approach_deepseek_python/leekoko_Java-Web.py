from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MySQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Tomcat, Apache
from diagrams.programming.framework import Spring
from diagrams.programming.language import Java, Javascript
from diagrams.generic.os import Windows
from diagrams.onprem.security import Vault
from diagrams.onprem.queue import Kafka
from diagrams.onprem.container import Docker

with Diagram("Multi-Tier Java Web Architecture", show=False, direction="TB"):
    with Cluster("Frontend Layer"):
        browser = Windows("Web Browser")
        jquery = Javascript("jQuery")
        html_css = Apache("HTML/CSS")
        
        browser >> jquery
        browser >> html_css

    with Cluster("Application Layer"):
        with Cluster("Java Web Applications"):
            servlets = Java("Servlets")
            jsp = Java("JSP")
            spring_boot = Spring("Spring Boot")
            tomcat = Tomcat("Tomcat Server")
            
            servlets >> jsp
            spring_boot >> tomcat

    with Cluster("Business Logic Layer"):
        with Cluster("Dubbo Framework"):
            dubbo_registry = Server("Registry")
            dubbo_rpc = Server("RPC")
            extension_loader = Server("Extension Loader")
            
            dubbo_registry >> dubbo_rpc
            dubbo_rpc >> extension_loader

    with Cluster("Data Layer"):
        mysql = MySQL("MySQL Database")
        redis = Redis("Redis Cache")
        
    with Cluster("Security Layer"):
        shiro = Vault("Apache Shiro")
        oauth = Server("OAuth2")

    with Cluster("Infrastructure"):
        docker = Docker("Container Runtime")
        kafka = Kafka("Message Queue")

    browser >> tomcat
    tomcat >> servlets
    tomcat >> spring_boot
    servlets >> dubbo_rpc
    spring_boot >> dubbo_rpc
    dubbo_rpc >> mysql
    dubbo_rpc >> redis
    tomcat >> shiro
    shiro >> oauth
    spring_boot >> kafka
    dubbo_rpc >> docker