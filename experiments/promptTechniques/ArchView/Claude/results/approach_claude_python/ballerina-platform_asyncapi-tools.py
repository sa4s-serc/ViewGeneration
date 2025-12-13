from plantuml import PlantUML

def generate_architecture_diagram():
    # Define the PlantUML diagram URL
    puml = PlantUML('http://www.plantuml.com/plantuml/img/')

    diagram = """
@startuml
skinparam componentStyle uml2
skinparam component {
    BackgroundColor<<AsyncAPI>> LightBlue
    BackgroundColor<<Core>> LightGreen
    BackgroundColor<<WebSocket>> LightYellow
}

package "AsyncAPI Tools" {
    [AsyncAPI/OpenAPI Code Generator] <<AsyncAPI>> as generator
    [Ballerina to AsyncAPI Export] <<AsyncAPI>> as exporter
    [WebSocket Support] <<WebSocket>> as websocket
    [Authentication Handler] <<Core>> as auth
    [Data Structure Handler] <<Core>> as data
    [Error Handler] <<Core>> as error
    [CLI Tool] <<Core>> as cli

    database "API Definitions" as apiDefs {
        [YAML Files] as yaml
    }

    database "Generated Code" as genCode {
        [Ballerina Files] as bal
    }

    cli --> generator : "Generate code"
    cli --> exporter : "Export spec"
    
    generator --> websocket : "Handle WebSocket"
    generator --> auth : "Handle auth"
    generator --> data : "Process types"
    generator --> error : "Handle errors"
    
    exporter --> websocket : "Handle WebSocket"
    exporter --> auth : "Handle auth"
    exporter --> data : "Process types" 
    exporter --> error : "Handle errors"

    yaml --> generator : "Input"
    generator --> bal : "Output"
    bal --> exporter : "Input"
    exporter --> yaml : "Output"
}

legend right
    |Color|Type|
    |<#LightBlue>|AsyncAPI Components|
    |<#LightGreen>|Core Components|
    |<#LightYellow>|WebSocket Components|
endlegend

caption Architecture diagram showing core components and data flow of AsyncAPI Tools

@enduml
"""

    # Save diagram to file
    with open('architecture.puml', 'w') as f:
        f.write(diagram)

    # Generate image
    puml.processes_file('architecture.puml', 'architecture.png')

if __name__ == "__main__":
    generate_architecture_diagram()