from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Redis, Memcached
from diagrams.onprem.network import Apache
from diagrams.programming.language import CSharp
from diagrams.generic.database import SQL
from diagrams.generic.storage import Storage
from diagrams.generic.network import Firewall
from diagrams.generic.os import LinuxGeneral

with Diagram("IRMA Web Service Framework Architecture", show=False, direction="TB"):
    web_server = Apache("Web Server\n(Apache/Nginx)")
    
    with Cluster("IRMA Core Engine (irmacall)"):
        irmacall = Server("irmacall\nMulti-threaded Engine")
        fastcgi = Server("FastCGI\nInterface")
        buffer_pool = Storage("Buffer Pool\nManagement")
        fuse = Firewall("Fuse\nCircuit Breaker")
        
        with Cluster("Core Services"):
            request_handler = Server("Request\nHandler")
            http_client = Server("HTTP Client\n(Fetcher)")
            kv_store = SQL("Key-Value\nStore Abstraction")
            logging = Server("Logging\nSystem")
            smtp = Server("SMTP\nSupport")
            crypto = Server("Cryptography\n(OpenSSL)")
            dns = Server("Async DNS\nResolution")
    
    with Cluster("IRMAKit Framework (C#)"):
        irmakit = CSharp("irmakit\nC# Framework")
        
        with Cluster("Application Components"):
            config = Server("Configuration\nSystem")
            session_mgmt = Server("Session\nManagement")
            routing = Server("Attribute\nRouting")
            templates = Server("Template\nEngine")
            utilities = Server("Utilities\n(Encryption, QR, etc)")
    
    with Cluster("External Services"):
        external_kv = [Redis("Redis"), Memcached("Memcached")]
        external_http = Server("External\nHTTP Services")
        email_service = Server("SMTP\nServer")
    
    with Cluster("Sample Application"):
        sample_app = CSharp("SampleService")
        rest_api = Server("REST API\nHandlers")
        static_content = Server("Static\nContent")
        auth = Server("Authentication")
    
    web_server >> fastcgi
    fastcgi >> irmacall
    irmacall >> request_handler
    irmacall >> http_client
    irmacall >> kv_store
    irmacall >> logging
    irmacall >> smtp
    irmacall >> crypto
    irmacall >> dns
    irmacall >> buffer_pool
    irmacall >> fuse
    
    irmacall >> irmakit
    irmakit >> config
    irmakit >> session_mgmt
    irmakit >> routing
    irmakit >> templates
    irmakit >> utilities
    
    session_mgmt >> external_kv
    http_client >> external_http
    smtp >> email_service
    
    irmakit >> sample_app
    sample_app >> rest_api
    sample_app >> static_content
    sample_app >> auth