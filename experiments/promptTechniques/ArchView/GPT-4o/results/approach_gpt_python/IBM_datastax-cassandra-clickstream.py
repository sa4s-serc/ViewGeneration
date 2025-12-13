from diagrams import Diagram, Cluster, Edge
from diagrams.generic.network import Router
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Cassandra
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Nodejs
from diagrams.programming.framework import React

with Diagram("Clickstream Data Capture and Analysis Architecture", show=False):
    user = User("User")

    with Cluster("Frontend"):
        nextjs = React("Next.js/React")
        nextjs_auth = Nodejs("NextAuth")
        user >> Edge(label="HTTP") >> nextjs

    with Cluster("Backend"):
        api_routes = Nodejs("Next.js API Routes")
        clicks_service = Nodejs("clicks.service.js")

        nextjs >> Edge(label="API Call") >> api_routes
        api_routes >> clicks_service

    with Cluster("Database"):
        cassandra = Cassandra("DSE/Cassandra")
        clicks_service >> Edge(label="DataStax Driver") >> cassandra

    with Cluster("Deployment"):
        ibm_cloud = Docker("IBM Cloud")
        openshift = Docker("OpenShift")

        api_routes >> Edge(label="Deploy") >> ibm_cloud
        api_routes >> Edge(label="Deploy") >> openshift

    with Cluster("Components"):
        app_header = Nodejs("AppHeader.jsx")
        category = Nodejs("Category.jsx")
        product_card = Nodejs("ProductCard.jsx")

        nextjs >> app_header
        nextjs >> category
        nextjs >> product_card

    with Cluster("State Management"):
        redux = Nodejs("Redux Store")
        cart_slice = Nodejs("cart.slice.js")

        nextjs >> redux
        redux >> cart_slice

    user << Edge(label="View Products") >> nextjs
    user << Edge(label="Add to Cart") >> nextjs
    user << Edge(label="View Cart") >> nextjs
    user << Edge(label="Sign In/Out") >> nextjs_auth