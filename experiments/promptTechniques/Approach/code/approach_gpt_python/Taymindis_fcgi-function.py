from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Nginx, Apache
from diagrams.onprem.compute import Server
from diagrams.programming.language import C, Cpp
from diagrams.onprem.container import Docker
from diagrams.programming.flowchart import Decision, Action, Collate

with Diagram("FastCGI Function Handler Framework", show=False):
    web_servers = [Nginx("Nginx"), Apache("Apache")]
    
    with Cluster("FastCGI Middleware"):
        fcgi = Server("FastCGI")
        config = Collate("Function Mapping\n(ffunc_config_t)")
        threading = Collate("Multi-threading")
        
    with Cluster("Application Logic"):
        handler_c = C("C Function Handlers")
        handler_cpp = Cpp("C++ Function Handlers")
        
    with Cluster("Deployment"):
        docker = Docker("Docker")
        cmake = Action("CMake")
        
    docs = Collate("README.md")
    docker_files = Collate("DockerExample/*")
    
    web_servers >> Edge(label="HTTP requests") >> fcgi
    fcgi >> Edge(label="Function mapping") >> config
    fcgi >> Edge(label="Request handling") >> [handler_c, handler_cpp]
    fcgi >> Edge(label="Thread management") >> threading
    docker >> Edge(label="Deployment") >> fcgi
    cmake >> Edge(label="Build") >> [handler_c, handler_cpp]
    docs >> Edge(label="Instructions") >> docker_files