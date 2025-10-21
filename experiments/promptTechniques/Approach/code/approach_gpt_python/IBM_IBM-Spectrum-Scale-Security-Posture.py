import plantuml

diagram = """
@startuml

skinparam componentStyle rectangle
skinparam monochrome true

package "IBM Spectrum Scale Security Posture Monitoring System" {
    
    component "collector/security_posture.py" as C1
    component "split_json_for_kibana.py" as C2
    component "fetch_security_posture_and_upload_to_ES.sh" as C3
    component "cronjob.py" as C4
    component "security-posture.conf" as C5
    component "scale-clusters.conf" as C6
    component "SecurityPostureArchitecture.xml" as C7
    component "README.md" as C8
    component "LICENSE" as C9
    component "collector/__init__.py" as C10

    C1 --> C2 : JSON Output
    C2 --> C3 : Splitted JSON
    C3 --> C5 : Reads Config
    C3 --> C6 : Reads Config
    C4 --> C3 : Trigger
    C3 --> "Elasticsearch" : Upload JSON
    C4 ..> C3 : Schedule

    database "Elasticsearch" {
        [Kibana] --> [Dashboard]
    }
    
    C5 ..> [Elasticsearch]
    C6 ..> [IBM Spectrum Scale Cluster]
    
    [IBM Spectrum Scale Cluster] ..> C1 : "mm" commands
    [Dashboard] ..> Kibana : Visualization

}

@enduml
"""

# Render the diagram
with open('architecture_diagram.png', 'wb') as out_file:
    plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/').processes(diagram, out_file=out_file)