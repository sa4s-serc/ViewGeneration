from diagrams import Diagram
from diagrams.aws.general import User
from diagrams.onprem.network import Apache
from diagrams.onprem.vcs import Git
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import Postgresql
from diagrams.aws.security import CertificateManager, IdentityAndAccessManagementIam
from diagrams.aws.management import Opsworks
from diagrams.aws.integration import StepFunctions
from diagrams.aws.compute import Lambda

with Diagram("Matryx Platform Architecture", show=False):
    user = User("User")
    frontend = Apache("Frontend")
    vcs = Git("Version Control System")
    
    ethereum_blockchain = Lambda("Ethereum Blockchain")
    cert_manager = CertificateManager("TLS/SSL")
    iam = IdentityAndAccessManagementIam("Access Management")
    opsworks = Opsworks("Deployment & Management")
    step_functions = StepFunctions("Workflow Management")
    
    db = Postgresql("Database")
    cache = Redis("Cache")

    user >> frontend >> vcs
    frontend >> ethereum_blockchain
    frontend >> cert_manager
    frontend >> iam
    frontend >> opsworks
    frontend >> step_functions

    ethereum_blockchain >> db
    ethereum_blockchain >> cache