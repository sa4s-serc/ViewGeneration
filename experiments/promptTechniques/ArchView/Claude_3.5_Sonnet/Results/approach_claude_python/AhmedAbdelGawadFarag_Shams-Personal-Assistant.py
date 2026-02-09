from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.onprem.compute import Server
from diagrams.azure.compute import ContainerInstances
from diagrams.firebase.develop import Functions
from diagrams.aws.network import APIGateway
from diagrams.onprem.database import MongoDB
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python
from diagrams.azure.ml import CognitiveServices

with Diagram("Shams Arabic Virtual Assistant Architecture", show=False):
    api = APIGateway("API Gateway")
    
    android = Server("Android App")
    
    main_server = ContainerInstances("Main Server")
    ner_server = ContainerInstances("NER Server")
    
    speech = CognitiveServices("Speech Services")
    
    db = MongoDB("MongoDB")
    queue = Kafka("Kafka")
    
    intent = Lambda("Intent Classification")
    nlp = Functions("NLP Processing")
    
    android >> api >> main_server
    main_server >> speech
    main_server >> queue >> nlp
    nlp >> ner_server
    ner_server >> db
    main_server >> intent
    intent >> db