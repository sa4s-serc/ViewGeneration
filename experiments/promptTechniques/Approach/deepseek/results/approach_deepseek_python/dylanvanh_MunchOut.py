from diagrams import Diagram, Cluster
from diagrams.programming.framework import Flutter, Flask
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Python, Dart

with Diagram("MunchOut Application Architecture", show=False, direction="TB"):
    with Cluster("Frontend (Flutter)"):
        frontend = Flutter("MunchOut App")
        
        with Cluster("Authentication"):
            auth_bloc = Flutter("AuthBloc")
            login_bloc = Flutter("LoginBloc")
            signup_bloc = Flutter("SignupBloc")
        
        with Cluster("Repositories"):
            user_repo = Flutter("UserRepository")
            restaurant_repo = Flutter("RestaurantRepository")
            customer_repo = Flutter("CustomerRepository")
        
        with Cluster("Packages"):
            flask_api = Flutter("flask_api")
            user_repo_pkg = Flutter("user_repository")
            restaurant_repo_pkg = Flutter("restaurant_repository")
            customer_repo_pkg = Flutter("customer_repository")
        
        with Cluster("Features"):
            restaurant_features = Flutter("Restaurant Features")
            customer_features = Flutter("Customer Features")

    with Cluster("Backend (Flask)"):
        backend = Flask("Flask API Server")
        
        with Cluster("API Resources"):
            customer_api = Flask("Customer API")
            restaurant_api = Flask("Restaurant API")
            event_api = Flask("Event API")
            booking_api = Flask("Booking API")
        
        with Cluster("Data Models"):
            customer_model = PostgreSQL("Customer Model")
            restaurant_model = PostgreSQL("Restaurant Model")
            event_model = PostgreSQL("Event Model")
            booking_model = PostgreSQL("Booking Model")

    database = PostgreSQL("Database")

    # Frontend internal connections
    frontend >> auth_bloc
    auth_bloc >> [login_bloc, signup_bloc]
    frontend >> [restaurant_features, customer_features]
    restaurant_features >> restaurant_repo
    customer_features >> customer_repo
    [user_repo, restaurant_repo, customer_repo] >> flask_api
    
    # Frontend to Backend connections
    flask_api >> backend
    
    # Backend internal connections
    backend >> [customer_api, restaurant_api, event_api, booking_api]
    customer_api >> customer_model
    restaurant_api >> restaurant_model
    event_api >> event_model
    booking_api >> booking_model
    
    # Backend to Database connections
    [customer_model, restaurant_model, event_model, booking_model] >> database