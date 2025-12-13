from diagrams import Diagram, Cluster, Edge
from diagrams.generic.database import SQL
from diagrams.generic.blank import Blank
from diagrams.onprem.client import User
from diagrams.programming.language import Javascript
from diagrams.onprem.compute import Server

with Diagram("Yoshixmk Remarks Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Chrome Extension"):
        chrome_extension = Javascript("popup.html\npopup.css\nrecord.js")
        user >> Edge(label="Records utterances") >> chrome_extension

    with Cluster("Web Server (Deno)"):
        server = Server("server.ts")
        handlers = [
            Javascript("homePage.jsx"),
            Javascript("tripPage.jsx"),
            Javascript("quotes.ts"),
            Javascript("remarks.ts"),
            Javascript("css.js")
        ]
        server - Edge(color="blue", style="dashed") - handlers

    with Cluster("Data Persistence"):
        faunadb = SQL("FaunaDB")
        gql_schema = Blank("schema.gql")

    chrome_extension >> Edge(label="Sends data") >> server
    server >> Edge(label="GraphQL Queries", color="purple") >> faunadb
    faunadb - Edge(label="Schema", style="dotted") - gql_schema

    with Cluster("Blog"):
        gitpress = Blank("GitPress Blog")
        md_sources = Blank("source/*.md")

    server >> Edge(label="Fetch travelogue", style="dashed") >> gitpress
    gitpress - Edge(style="dotted") - md_sources

    user << Edge(label="Displays remarks", color="green") << server