from diagrams import Diagram
from diagrams.generic.blank import Blank
from diagrams.programming.framework import Angular
from diagrams.programming.language import TypeScript
from diagrams.onprem.client import Users

with Diagram("Angular Interview Q&A Architecture", show=False, direction="LR"):
    users = Users("Interview Candidates")
    
    angular_app = Angular("Angular Q&A Application")
    
    components = TypeScript("Components & Directives")
    services = TypeScript("Services & Dependency Injection")
    routing = TypeScript("Routing & Navigation")
    modules = TypeScript("Modules & Lazy Loading")
    
    users >> angular_app
    
    angular_app >> components
    angular_app >> services
    angular_app >> routing
    angular_app >> modules