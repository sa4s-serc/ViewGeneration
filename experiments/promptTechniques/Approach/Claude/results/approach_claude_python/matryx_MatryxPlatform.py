from diagrams import Diagram
from diagrams.programming.language import Python
from diagrams.onprem.database import Postgresql
from diagrams.aws.blockchain import ManagedBlockchain
from diagrams.aws.security import IAM
from diagrams.aws.integration import SNS

with Diagram("Matryx Platform Architecture", show=False):
    # Core Platform Components
    platform = Python("MatryxPlatform")
    db = Postgresql("Data Storage")
    blockchain = ManagedBlockchain("Smart Contracts")
    
    # Security & Integration
    auth = IAM("Access Control") 
    events = SNS("Event Notifications")

    # Core Flow
    platform >> auth >> blockchain
    platform >> db
    blockchain >> events
    events >> platform

    # Data Flow
    db << platform
    blockchain << platform