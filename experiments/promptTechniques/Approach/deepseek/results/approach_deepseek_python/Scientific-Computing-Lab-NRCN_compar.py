from diagrams import Diagram
from diagrams.programming.framework import Angular, Flask, Django
from diagrams.programming.language import JavaScript, Python, Java, Cpp
from diagrams.onprem.database import MongoDB
from diagrams.onprem.network import Nginx
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS

with Diagram("CodeMirror and ComPar Architecture", show=False, direction="TB"):
    # Frontend components
    frontend = Angular("Web GUI")
    codemirror = JavaScript("CodeMirror Editor")
    
    # Backend components
    backend = Flask("ComPar Backend")
    jinja = Django("Jinja2 Templates")
    
    # Compiler components
    compilers = [
        Python("GCC Compiler"),
        Python("ICC Compiler"),
        Python("Cetus"),
        Python("Autopar"),
        Python("Par4all")
    ]
    
    # Database and storage
    mongodb = MongoDB("MongoDB")
    rds = RDS("Results DB")
    
    # Infrastructure components
    nginx = Nginx("Web Server")
    jenkins = Jenkins("CI/CD")
    docker = Docker("Container Runtime")
    ec2 = EC2("Compute Instances")
    elb = ELB("Load Balancer")
    
    # Connections
    frontend >> codemirror
    frontend >> backend
    backend >> jinja
    backend >> compilers
    backend >> mongodb
    backend >> rds
    nginx >> frontend
    jenkins >> docker
    docker >> ec2
    elb >> nginx