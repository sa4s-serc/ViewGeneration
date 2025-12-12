from diagrams import Diagram, Cluster
from diagrams.gcp.compute import AppEngine 
from diagrams.firebase.develop import Authentication
from diagrams.aws.storage import Storage
from diagrams.onprem.vcs import Github
from diagrams.generic.device import Mobile
from diagrams.programming.framework import React

with Diagram("Remarks System Architecture", show=False, direction="LR"):
    with Cluster("Client Side"):
        browser = Mobile("Web Browser")
        chrome_ext = React("Chrome Extension")

    with Cluster("Server Side"):
        deno_server = AppEngine("Deno Server")
        auth = Authentication("Auth")
        
        with Cluster("Data Storage"):
            fauna = Storage("FaunaDB")
            db = Storage("Database")

    with Cluster("Content"):
        gitpress = Github("GitPress Blog")

    # Flow
    browser >> chrome_ext >> deno_server
    chrome_ext >> fauna
    deno_server >> auth
    deno_server >> db
    deno_server >> gitpress
    browser >> gitpress