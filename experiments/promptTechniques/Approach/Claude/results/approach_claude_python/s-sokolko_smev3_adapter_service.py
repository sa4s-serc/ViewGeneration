from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.onprem.database import MongoDB
from diagrams.onprem.network import Nginx
from diagrams.generic.network import Switch
from diagrams.generic.compute import Rack

def generate_architecture_diagram():
    with Diagram("SMEV3 Adapter Service Architecture", show=False, direction="TB"):
        
        # External systems
        clients = Rack("Client Applications")
        smev3 = Rack("SMEV3 Adapter")
        
        with Cluster("SMEV3 Adapter Service"):
            # API Layer
            api = Nginx("API Layer\n(Sanic)")
            
            # Business Logic Layer
            with Cluster("Business Logic"):
                business = Python("Query Processor")
                schema = Python("Schema Validator")
                smev_client = Python("SMEV3 Client")
            
            # Data Layer
            db = MongoDB("MongoDB")
            
        # Draw relationships
        clients >> api
        api >> business
        business >> schema
        business >> smev_client
        business >> db
        smev_client >> smev3

if __name__ == "__main__":
    generate_architecture_diagram()