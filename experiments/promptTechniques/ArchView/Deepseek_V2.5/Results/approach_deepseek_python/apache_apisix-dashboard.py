from diagrams import Diagram
from diagrams.programming.framework import React, Flask
from diagrams.programming.language import TypeScript, JavaScript
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git

with Diagram("Apache APISIX Dashboard Frontend Architecture", show=False, direction="TB"):
    users = Users("End Users")
    
    with Diagram("Frontend Layer"):
        react_app = React("React Application")
        typescript = TypeScript("TypeScript")
        javascript = JavaScript("JavaScript")
        
        react_app >> typescript
        react_app >> javascript
    
    with Diagram("UI Components"):
        mantine_ui = React("Mantine UI")
        ant_design = React("Ant Design Pro")
        react_router = React("TanStack Router")
        react_query = React("TanStack Query")
        
        react_app >> mantine_ui
        react_app >> ant_design
        react_app >> react_router
        react_app >> react_query
    
    with Diagram("State Management"):
        mobx = React("MobX Stores")
        form_management = React("React Hook Form")
        
        react_app >> mobx
        react_app >> form_management
    
    with Diagram("API Layer"):
        axios = React("Axios Client")
        api_hooks = React("Custom Hooks")
        
        react_app >> axios
        react_app >> api_hooks
    
    with Diagram("Backend Services"):
        apisix_api = Flask("APISIX Admin API")
        postgresql = PostgreSQL("Configuration DB")
        redis = Redis("Cache")
        
        axios >> apisix_api
        apisix_api >> postgresql
        apisix_api >> redis
    
    with Diagram("Development Tools"):
        vite = React("Vite Build Tool")
        playwright = React("Playwright E2E Tests")
        
        react_app >> vite
        react_app >> playwright
    
    with Diagram("CI/CD Pipeline"):
        jenkins = Jenkins("Jenkins CI")
        docker = Docker("Docker")
        git = Git("Git Repository")
        
        jenkins >> docker
        git >> jenkins
    
    with Diagram("Monitoring"):
        grafana = Grafana("Grafana")
        prometheus = Prometheus("Prometheus")
        loki = Loki("Loki Logs")
        
        react_app >> prometheus
        apisix_api >> prometheus
        prometheus >> grafana
        react_app >> loki
        apisix_api >> loki
    
    users >> react_app