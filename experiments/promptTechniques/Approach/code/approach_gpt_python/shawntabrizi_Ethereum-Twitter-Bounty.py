from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.programming.language import JavaScript
from diagrams.programming.language import HTML
from diagrams.onprem.client import User
from diagrams.generic.network import Blockchain

with Diagram("Twitter Bounty dApp Architecture", show=False):
    
    user = User("User")
    
    with Cluster("Front-End"):
        frontend = HTML("HTML + CSS")
        web3js = JavaScript("Web3.js")
        jquery = JavaScript("jQuery")
        user >> Edge(label="Interacts") >> frontend

    with Cluster("Smart Contracts"):
        twitter_bounty = Custom("TwitterBounty.sol", "./icons/solidity.png")
        twitter_oracle = Custom("TwitterOracle.sol", "./icons/solidity.png")
        
        frontend >> Edge(label="Calls", style="dashed") >> web3js >> twitter_bounty
        twitter_bounty >> Edge(label="Uses", style="dashed") >> twitter_oracle

    with Cluster("Truffle Suite"):
        truffle_contract = Custom("TruffleContract", "./icons/truffle.png")
        
        truffle_contract >> Edge(label="Interacts") >> twitter_bounty

    with Cluster("Blockchain"):
        ethereum = Blockchain("Ethereum")
        
        twitter_bounty >> Edge(label="Executes") >> ethereum
        twitter_oracle >> Edge(label="Fetches Tweet", style="dotted") >> ethereum

    with Cluster("Oracle Service"):
        provable_things = Custom("Provable", "./icons/provable.png")
        
        twitter_oracle >> Edge(label="Retrieves Data", style="dotted") >> provable_things