from diagrams import Diagram, Cluster
from diagrams.programming.framework import Flutter
from diagrams.programming.language import Dart
from diagrams.firebase.develop import Authentication, Functions, RealtimeDatabase
from diagrams.onprem.monitoring import Sentry
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import Graphql
from diagrams.onprem.database import Postgresql

with Diagram("Facebook Clone Clean Architecture", show=False):
    with Cluster("Presentation Layer"):
        ui = Flutter("UI Components")
        bloc = Flutter("BLoC State Management")

    with Cluster("Domain Layer"):
        usecases = Dart("Use Cases")
        entities = Dart("Entities")

    with Cluster("Data Layer"):
        repos = Dart("Repositories")
        datasources = Dart("Data Sources")

    with Cluster("Infrastructure"):
        db = Postgresql("PostgreSQL")
        cache = Redis("Cache")
        auth = Authentication("Firebase Auth")
        rtdb = RealtimeDatabase("Firebase RTDB")
        fn = Functions("Cloud Functions")
        api = Graphql("GraphQL API")
        monitor = Sentry("Error Monitoring")

    # Flow
    ui >> bloc >> usecases
    usecases >> entities
    usecases >> repos
    repos >> datasources
    
    # Infrastructure connections
    datasources >> db
    datasources >> cache
    datasources >> auth
    datasources >> rtdb
    datasources >> fn
    datasources >> api
    bloc >> monitor