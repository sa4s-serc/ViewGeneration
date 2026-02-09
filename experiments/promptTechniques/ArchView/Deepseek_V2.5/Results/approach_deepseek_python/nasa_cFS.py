from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql

with Diagram("NASA cFS Architecture View", show=False, direction="TB"):
    with Cluster("CI/CD Pipeline"):
        jenkins = Jenkins("Jenkins")
        with Cluster("Static Analysis"):
            cppcheck = Server("Cppcheck")
            codeql = Server("CodeQL")
            misra = Server("MISRA")
        with Cluster("Testing"):
            unit_tests = Server("Unit Tests")
            functional_tests = Server("Functional Tests")
            cross_platform = Server("Cross-Platform Tests")
    
    with Cluster("Core Flight System (cFS)"):
        with Cluster("cFE Framework"):
            es = Server("Event Services")
            osal = Server("OSAL")
            psp = Server("PSP")
        
        with Cluster("Applications"):
            lab_apps = Server("Lab Applications")
            custom_apps = Server("Custom Applications")
        
        with Cluster("Tools"):
            bundler = Server("Bundler")
            host_tools = Server("Host Tools")
    
    with Cluster("Monitoring & Logging"):
        grafana = Grafana("Grafana")
        prometheus = Prometheus("Prometheus")
    
    # CI/CD connections
    jenkins >> [cppcheck, codeql, misra]
    jenkins >> [unit_tests, functional_tests, cross_platform]
    
    # Core system connections
    es >> osal
    osal >> psp
    bundler >> [lab_apps, custom_apps]
    host_tools >> [lab_apps, custom_apps]
    
    # Monitoring connections
    [es, osal, psp, lab_apps, custom_apps] >> prometheus
    prometheus >> grafana