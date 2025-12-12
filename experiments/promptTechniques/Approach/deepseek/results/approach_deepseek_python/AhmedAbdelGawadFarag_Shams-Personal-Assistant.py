from diagrams import Diagram
from diagrams.generic.device import Mobile
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import Postgresql
from diagrams.onprem.network import Internet
from diagrams.gcp.ml import SpeechToText, TextToSpeech
from diagrams.aws.ml import Comprehend
from diagrams.programming.framework import Flask

with Diagram("Shams Arabic Virtual Assistant Architecture", show=False):
    user = Client("User")
    internet = Internet("Internet")
    
    android_app = Mobile("Android App")
    
    with Diagram("Backend Services"):
        main_server = Flask("Main Server")
        ner_server = Flask("NER Server")
        
        with Diagram("Cloud Services"):
            stt = SpeechToText("Google Cloud STT")
            tts = TextToSpeech("Google Cloud TTS")
            comprehend = Comprehend("Intent Classification")
        
        with Diagram("Data Storage"):
            postgres = Postgresql("Database")
            redis = Redis("Cache")
    
    user >> internet >> android_app
    android_app >> main_server
    android_app >> ner_server
    
    main_server >> stt
    main_server >> tts
    main_server >> comprehend
    main_server >> postgres
    main_server >> redis
    
    ner_server >> comprehend
    ner_server >> postgres