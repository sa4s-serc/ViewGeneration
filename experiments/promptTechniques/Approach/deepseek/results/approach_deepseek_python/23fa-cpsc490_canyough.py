from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.client import User

with Diagram("Twitter Recommendation System Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Frontend Layer"):
        lb = ELB("Load Balancer")
        web_servers = [EC2("Web Server 1"), EC2("Web Server 2")]
    
    with Cluster("Application Layer"):
        with Cluster("Product Mixer"):
            product_mixer = EC2("Product Mixer")
        
        with Cluster("CR Mixer"):
            cr_mixer = EC2("CR Mixer")
        
        with Cluster("Home Mixer"):
            home_mixer = EC2("Home Mixer")
        
        with Cluster("FRS"):
            frs = EC2("Follow Recommendations Service")
    
    with Cluster("Data Layer"):
        with Cluster("Candidate Sources"):
            earlybird = EC2("Earlybird")
            simclusters = EC2("SimClusters")
            user_graph = EC2("User Tweet Graph")
        
        with Cluster("Feature Stores"):
            feature_store = RDS("Feature Store")
        
        with Cluster("ML Services"):
            navi = EC2("Navi ML Server")
        
        with Cluster("Storage"):
            s3_storage = S3("Object Storage")
            cache = EC2("Cache")

    user >> lb >> web_servers
    web_servers >> product_mixer
    product_mixer >> cr_mixer
    product_mixer >> home_mixer
    product_mixer >> frs
    
    cr_mixer >> earlybird
    cr_mixer >> simclusters
    cr_mixer >> user_graph
    cr_mixer >> feature_store
    cr_mixer >> navi
    
    home_mixer >> feature_store
    home_mixer >> cache
    home_mixer >> s3_storage
    
    frs >> feature_store
    frs >> cache