from diagrams import Diagram
from diagrams.aws.security import KMS
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.aws.compute import Lambda
from diagrams.aws.management import Cloudwatch

with Diagram("Sneaker Architecture", show=False, direction="TB"):
    user = User("User")
    cli = Lambda("CLI (sneaker)")
    
    manager = Lambda("Manager")
    envelope = Lambda("Envelope")
    kms = KMS("KeyManagement")
    s3 = S3("ObjectStorage")
    
    user >> cli
    cli >> manager
    
    manager >> envelope
    manager >> kms
    manager >> s3
    
    envelope >> kms