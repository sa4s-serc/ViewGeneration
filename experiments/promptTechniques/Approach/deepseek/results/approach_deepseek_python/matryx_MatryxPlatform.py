from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MongoDB
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import Javascript
from diagrams.custom import Custom

with Diagram("Matryx Platform Architecture", show=False, direction="TB"):
    users = User("Users")
    
    with Diagram("Frontend Layer"):
        web_ui = Nginx("Web UI")
        js_interaction = Javascript("JS Interaction Layer")
        
    with Diagram("Smart Contract Layer"):
        ethereum = Custom("Ethereum Blockchain", "./ethereum.png")
        
        with Diagram("Core Contracts"):
            platform = Custom("MatryxPlatform", "./solidity.png")
            forwarder = Custom("MatryxForwarder", "./solidity.png")
            token = Custom("MatryxToken", "./solidity.png")
            system = Custom("MatryxSystem", "./solidity.png")
            
        with Diagram("Library Contracts"):
            lib_platform = Custom("LibPlatform", "./solidity.png")
            lib_commit = Custom("LibCommit", "./solidity.png")
            lib_tournament = Custom("LibTournament", "./solidity.png")
    
    with Diagram("Data Layer"):
        mongodb = MongoDB("MongoDB")
        redis = Redis("Redis Cache")
    
    with Diagram("Testing/Deployment"):
        truffle = Server("Truffle Framework")
        tests = Javascript("Test Scripts")
        benchmarks = Javascript("Benchmark Scripts")
    
    users >> web_ui
    web_ui >> js_interaction
    js_interaction >> ethereum
    
    forwarder >> platform
    platform >> [lib_platform, lib_commit, lib_tournament]
    platform >> system
    token >> platform
    
    js_interaction >> mongodb
    js_interaction >> redis
    
    truffle >> [tests, benchmarks]
    tests >> ethereum
    benchmarks >> ethereum