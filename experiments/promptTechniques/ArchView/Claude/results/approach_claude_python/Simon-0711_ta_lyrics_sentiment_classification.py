from plantuml import PlantUML
from urllib.parse import quote
import os

def generate_architecture_diagram():
    diagram = """
@startuml
!define RECTANGLE class

skinparam componentStyle uml2
skinparam component {
    BackgroundColor White
    BorderColor Black
    ArrowColor Black
}

rectangle "Frontend (React)" as frontend {
    [User Interface]
    [Search Component]
    [Results Display]
}

rectangle "Backend (FastAPI)" as backend {
    [API Endpoints]
    [Lyrics Processing]
    [CNN Model Service]
    [Similarity Engine]
}

database "Elasticsearch" as es {
    [Song Lyrics Store]
    [Mood Index]
}

cloud "LyricsGenius API" as genius {
    [Lyrics Service]
}

rectangle "CNN Model" as cnn {
    [Word Embeddings]
    [Classification Layer]
}

frontend --> backend : HTTP/REST
backend --> es : Query/Store
backend --> genius : Fetch Lyrics
backend --> cnn : Classify Mood
es --> backend : Similar Songs

@enduml
"""
    
    # Create a temporary file
    with open("architecture.puml", "w") as f:
        f.write(diagram)

    # Generate the URL-encoded PlantUML diagram
    encoded_diagram = quote(diagram)
    
    # Create PlantUML object and generate diagram
    puml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    puml.processes_file("architecture.puml")

    # Clean up temporary file
    os.remove("architecture.puml")

if __name__ == "__main__":
    generate_architecture_diagram()