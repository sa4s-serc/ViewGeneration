from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS
from diagrams.aws.network import APIGateway
from diagrams.aws.database import RDS
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.analytics import EMR
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS

def generate_diagram():
    with Diagram("Twitter Recommendation System Architecture", show=False, direction="TB"):
        with Cluster("Data Processing Layer"):
            emr = EMR("Batch Processing")
            s3 = S3("Data Storage")
            
        with Cluster("Service Layer"):
            with Cluster("Product Mixer"):
                mixer = ECS("Product Mixer")
                cr_mixer = ECS("CR Mixer")
                home_mixer = ECS("Home Mixer")
            
            with Cluster("Recommendation Services"):
                frs = ECS("Follow Recommendations")
                model = SagemakerModel("ML Models")
            
            queue = SQS("Message Queue")
            api = APIGateway("API Gateway")
            db = RDS("User Data")
        
        # Data flow
        s3 >> emr
        emr >> model
        api >> mixer
        mixer >> cr_mixer
        mixer >> home_mixer
        cr_mixer >> model
        home_mixer >> model
        model >> frs
        frs >> queue
        queue >> mixer
        db >> mixer

if __name__ == "__main__":
    generate_diagram()