from diagrams import Diagram, Cluster
from diagrams.programming.framework import React
from diagrams.programming.language import Javascript
from diagrams.custom import Custom
from diagrams.aws.blockchain import ManagedBlockchain 
from diagrams.firebase.develop import Authentication
from diagrams.saas.cdn import Cloudflare
from diagrams.onprem.client import Users

# Create custom icons for components that don't have built-in nodes
with Diagram("Twitter Bounty dApp Architecture", show=False, direction="LR"):
    
    with Cluster("Frontend"):
        ui = React("Web UI")
        js = Javascript("web3.js")

    with Cluster("Backend"):
        with Cluster("Smart Contracts"):
            # Using Custom for Solidity contracts since no built-in node exists
            bounty = Custom("TwitterBounty", "./solidity.png")
            oracle = Custom("TwitterOracle", "./solidity.png")
        
        # Using ManagedBlockchain to represent Ethereum
        eth = ManagedBlockchain("Ethereum\nBlockchain")

    with Cluster("External Services"):
        auth = Authentication("User Auth")
        cdn = Cloudflare("CDN")
        chain = ManagedBlockchain("Oracle Service")

    users = Users("End Users")

    # Define relationships
    users >> cdn >> ui
    ui >> js
    js >> bounty
    js >> auth
    
    bounty >> oracle
    oracle >> chain
    
    bounty >> eth
    oracle >> eth