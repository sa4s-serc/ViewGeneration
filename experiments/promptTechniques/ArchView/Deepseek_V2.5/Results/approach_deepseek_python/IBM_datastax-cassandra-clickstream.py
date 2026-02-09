from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import Nextjs, React
from diagrams.onprem.database import Cassandra
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import Javascript

with Diagram("Clickstream Data Capture and Analysis Application", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        frontend = Nextjs("Next.js App")
        react = React("React Components")
        redux = Javascript("Redux Store")
        frontend >> react
        react >> redux
    
    with Cluster("Backend Layer"):
        with Cluster("API Routes"):
            api_auth = Nextjs("Auth API")
            api_products = Nextjs("Products API")
            api_history = Nextjs("History API")
            api_cart = Nextjs("Cart API")
        
        with Cluster("Services"):
            click_service = Javascript("Clicks Service")
            auth_service = Nextjs("NextAuth")
    
    with Cluster("Data Layer"):
        database = Cassandra("DataStax Enterprise")
        cache = Redis("Redis Cache")
    
    user >> frontend
    frontend >> api_auth
    frontend >> api_products
    frontend >> api_history
    frontend >> api_cart
    api_auth >> auth_service
    api_products >> click_service
    api_history >> click_service
    api_cart >> click_service
    click_service >> database
    click_service >> cache
    auth_service >> database