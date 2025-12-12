from diagrams import Diagram, Cluster
from diagrams.programming.framework import Rails
from diagrams.onprem.database import Mysql
from diagrams.programming.language import Javascript, Ruby
from diagrams.onprem.vcs import Github
from diagrams.saas.cdn import Cloudflare
from diagrams.onprem.network import Nginx
from diagrams.gcp.compute import Run

with Diagram("Bookshelf Web Architecture", show=False, direction="TB"):
    with Cluster("Frontend"):
        frontend = [
            Javascript("jQuery UI"),
            Javascript("Barcode Scanner JS")
        ]

    with Cluster("Application Layer"):
        rails = Rails("Rails App")
        api = Run("REST API")

    with Cluster("Data Layer"):
        db = Mysql("MySQL")

    with Cluster("External Services"):
        google_books = Run("Google Books API")
        oauth = Run("OAuth/Facebook")

    with Cluster("Infrastructure"):
        nginx = Nginx("Nginx")
        cdn = Cloudflare("CDN")

    with Cluster("Version Control"):
        github = Github("Source Code")

    # Connect components
    frontend[0] >> nginx
    frontend[1] >> nginx
    nginx >> rails
    rails >> api
    rails >> db
    rails >> google_books
    rails >> oauth
    cdn >> nginx