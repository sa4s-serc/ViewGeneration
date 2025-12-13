from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Internet
from diagrams.programming.flowchart import Action
from diagrams.generic.network import Router

with Diagram("Shams Arabic Virtual Assistant Architecture", show=False, direction="TB"):
    client = Client("Shams_Android")
    
    with Cluster("Backend Servers"):
        with Cluster("Main Server"):
            main_server = Server("Flask App")
            intent_classifier = Action("Intent Classification")
            stt = Action("Speech-to-Text")
            tts = Action("Text-to-Speech")
            translation = Action("Translation")

            main_server >> Edge(label="classifies") >> intent_classifier
            main_server >> Edge(label="converts") >> stt
            main_server >> Edge(label="converts") >> tts
            main_server >> Edge(label="translates") >> translation

        with Cluster("NER Server"):
            ner_server = Server("Flask App")
            ner_model = Action("NER Model")
            ner_server >> Edge(label="extracts") >> ner_model

    client >> Edge(label="HTTP") >> main_server
    client >> Edge(label="HTTP") >> ner_server
    main_server >> Edge(label="REST API") >> ner_server

    with Cluster("Google Cloud Services"):
        google_stt = Internet("Speech-to-Text API")
        google_tts = Internet("Text-to-Speech API")

        stt >> Edge(label="uses") >> google_stt
        tts >> Edge(label="uses") >> google_tts