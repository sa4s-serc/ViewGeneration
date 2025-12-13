from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress
from diagrams.k8s.others import CRD
from diagrams.onprem.network import Nginx
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Scala
from diagrams.programming.language import Javascript
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.security import Vault
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.ci import Jenkins

with Diagram("Fabric Gateway Architecture", show=False, direction="TB"):
    with Cluster("Kubernetes Cluster"):
        with Cluster("Gateway Operator"):
            operator = Pod("Gateway Operator")
            crd = CRD("FabricGateway CRD")
            webhook = Pod("Webhook Server")
            ingress_chain = Pod("IngressDerivationChain")
            stackset_ops = Pod("StackSetOperations")
            
        with Cluster("API Gateway"):
            skipper = Nginx("Skipper")
            ingress = Ingress("Ingress")
            
        with Cluster("Backend Services"):
            service1 = Pod("Service 1")
            service2 = Pod("Service 2")
            service3 = Pod("Service 3")
            
        with Cluster("StackSets"):
            stackset1 = Pod("StackSet 1")
            stackset2 = Pod("StackSet 2")
            
    with Cluster("External Services"):
        iam = Vault("IAM Service")
        e2e_tests = Pod("E2E Tests")
        docs = Pod("Documentation")
        search_worker = Javascript("Search Worker")
        license_mgmt = Pod("License Management")
        
    # Core relationships
    crd >> operator
    operator >> webhook
    operator >> ingress_chain
    operator >> stackset_ops
    ingress_chain >> skipper
    skipper >> ingress
    ingress >> [service1, service2, service3]
    stackset_ops >> [stackset1, stackset2]
    
    # External integrations
    skipper >> iam
    operator >> e2e_tests
    operator >> docs
    operator >> search_worker
    operator >> license_mgmt
    
    # Policy enforcement flow
    with Cluster("Policy Enforcement"):
        auth = Pod("Authentication")
        authz = Pod("Authorization")
        rate_limit = Pod("Rate Limiting")
        cors = Pod("CORS")
        
    skipper >> auth
    auth >> authz
    authz >> rate_limit
    rate_limit >> cors