from diagrams import Diagram, Cluster
from diagrams.aws.blockchain import Blockchain
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.onprem.vcs import Github
from diagrams.programming.language import JavaScript, Python
from diagrams.custom import Custom

with Diagram("Twitter Bounty dApp Architecture", show=False):
    user = Client("User")

    with Cluster("Front-End"):
        frontend = JavaScript("HTML/CSS/JavaScript")
        web3js = Custom("web3.js", "./web3js.png")
        frontend - web3js

    with Cluster("Smart Contracts"):
        twitter_bounty = Blockchain("TwitterBounty.sol")
        twitter_oracle = Blockchain("TwitterOracle.sol")

    with Cluster("Ethereum Blockchain"):
        ethereum = Blockchain("Ethereum")

    with Cluster("External Oracle Service"):
        oraclize = Custom("Provable Things", "./oraclize.png")

    with Cluster("Development & Deployment"):
        truffle = Custom("Truffle Framework", "./truffle.png")
        github = Github("Github")

    user >> frontend >> web3js >> twitter_bounty
    twitter_bounty >> twitter_oracle
    twitter_oracle >> oraclize
    twitter_bounty >> ethereum
    ethereum >> oraclize
    github >> truffle >> ethereum