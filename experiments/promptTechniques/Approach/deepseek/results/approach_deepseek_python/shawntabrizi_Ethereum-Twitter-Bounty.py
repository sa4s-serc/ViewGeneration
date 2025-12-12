from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.integration import Eventbridge
from diagrams.aws.security import Cognito
from diagrams.aws.management import Cloudwatch
from diagrams.generic.database import SQL
from diagrams.programming.framework import React

with Diagram("Twitter Bounty dApp Architecture", show=False, direction="TB"):
    user = User("User")
    
    frontend = React("Frontend UI")
    
    with Diagram("Web3 Layer"):
        web3 = Lambda("Web3 Integration")
        cognito = Cognito("Authentication")
    
    with Diagram("Smart Contract Layer"):
        twitter_bounty = SQL("TwitterBounty.sol")
        twitter_oracle = SQL("TwitterOracle.sol")
        provable = Lambda("Provable Oracle")
    
    with Diagram("Blockchain Layer"):
        ethereum = Lambda("Ethereum Network")
    
    with Diagram("Data Layer"):
        dynamodb = Dynamodb("Bounty Data")
        s3 = S3("Static Assets")
    
    with Diagram("Monitoring"):
        cloudwatch = Cloudwatch("Monitoring & Logging")
    
    user >> frontend
    frontend >> web3
    frontend >> cognito
    web3 >> twitter_bounty
    web3 >> twitter_oracle
    twitter_oracle >> provable
    provable >> ethereum
    twitter_bounty >> ethereum
    twitter_bounty >> dynamodb
    frontend >> s3
    web3 >> cloudwatch
    twitter_bounty >> cloudwatch
    twitter_oracle >> cloudwatch