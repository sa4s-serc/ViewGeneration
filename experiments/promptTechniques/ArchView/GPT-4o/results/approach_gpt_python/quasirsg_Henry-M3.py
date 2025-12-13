from diagrams import Diagram, Cluster
from diagrams.programming.language import JavaScript, Nodejs
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import MongoDB
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.ci import Jenkins
from diagrams.firebase.develop import Functions
from diagrams.firebase.grow import ABTesting
from diagrams.elastic.elasticsearch import Elasticsearch

with Diagram("Node.js/Express.js Learning Repository", show=False):
    with Cluster("Asynchronous Programming & Promises"):
        custom_promise = Functions("Custom $Promise Library")
        jasmine_matchers = ABTesting("Custom Jasmine Matchers")

    with Cluster("Node.js Fundamentals"):
        nodejs = Nodejs("Node.js")
        express = Functions("Express.js")
        nginx = Nginx("Nginx")
        mongodb = MongoDB("MongoDB")
        streams_buffers = Functions("Streams & Buffers")

    with Cluster("Express.js Web Application Development"):
        rest_apis = express
        middleware = Functions("Middleware")
        body_parser = Functions("Body-Parser")
        static_files = Functions("Static Files")

    with Cluster("Software Testing"):
        unit_testing = Jenkins("Unit Testing")
        integration_testing = Jenkins("Integration Testing")
        end_to_end_testing = Jenkins("End-to-End Testing")

    with Cluster("Important Files & Components"):
        pledge_js = Functions("pledge.js")
        custom_matchers_js = Functions("custom.matchers.js")
        index_js = Functions("index.js")
        myapp = Functions("myapp/")
        server_js = Functions("server.js")

    with Cluster("Architectural and Design Insights"):
        modular_architecture = Elasticsearch("Modular Architecture")
        layered_architecture = Elasticsearch("Layered Architecture")
        middleware_pattern = Elasticsearch("Middleware Pattern")
        event_driven = Elasticsearch("Event-Driven (Promises)")
        tdd = Functions("Test-Driven Development (TDD)")

    prometheus = Prometheus("Prometheus")
    modular_architecture >> prometheus
    layered_architecture >> prometheus
    middleware_pattern >> prometheus
    event_driven >> prometheus
    tdd >> prometheus

    # Connecting the clusters
    custom_promise >> jasmine_matchers
    nodejs >> express
    nodejs >> streams_buffers
    express >> [nginx, mongodb]
    rest_apis >> [middleware, body_parser, static_files]
    unit_testing >> integration_testing >> end_to_end_testing
    pledge_js >> custom_matchers_js
    index_js >> myapp >> server_js