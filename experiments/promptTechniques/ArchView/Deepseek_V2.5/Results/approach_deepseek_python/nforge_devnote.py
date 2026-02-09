from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.vcs import Git
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Javascript
from diagrams.generic.blank import Blank

with Diagram("NForge DevNote Architecture", show=False, direction="TB"):
    client = User("Client")
    
    with Cluster("Frontend"):
        browser = Javascript("Browser")
        jquery = Javascript("jQuery")
        bootstrap = Javascript("Bootstrap")
        codemirror = Javascript("CodeMirror")
        browser >> [jquery, bootstrap, codemirror]
    
    with Cluster("Backend"):
        nginx = Nginx("Nginx")
        with Cluster("Node.js Application"):
            app = Server("app.coffee")
            socketio = Server("Socket.IO")
            
            with Cluster("Application Modules"):
                wiki = Server("wikiApp.coffee")
                user = Server("userApp.coffee")
                file = Server("fileApp.coffee")
                admin = Server("adminApp.coffee")
                [wiki, user, file, admin] >> app
            
            with Cluster("Core Libraries"):
                gitfs = Server("gitfs.js")
                users = Server("users.js")
                renderer = Server("renderer.js")
                i18n = Server("i18n.js")
                [gitfs, users, renderer, i18n] >> app
    
    with Cluster("Data Storage"):
        git_repo = Git("Git Repository")
        redis = Redis("Redis")
    
    with Cluster("Testing"):
        mocha = Server("Mocha Tests")
        travis = Server("Travis CI")
    
    client >> nginx >> app
    app >> socketio
    app >> git_repo
    app >> redis
    app >> mocha
    mocha >> travis