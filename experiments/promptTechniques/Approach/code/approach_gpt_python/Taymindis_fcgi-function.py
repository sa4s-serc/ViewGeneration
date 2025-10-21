from plantuml import PlantUML

# Initialize plantuml diagram
diagram = """
@startuml

title FastCGI Function Handler Framework Architecture

package "Core Components" {
    component [FastCGI Integration] <<C>>
    component [Function Mapping] <<M>>
    component [Request Handling] <<R>>
    component [Multi-threading] <<T>>
    component [Configuration] <<C>>
}

package "Key Files" {
    component [ffunc.h] <<H>>
    component [ffunc.c] <<C>>
    component [CMakeLists.txt] <<B>>
    component [profile_service.c/cpp] <<E>>
    component [DockerExample/*] <<D>>
    component [README.md] <<D>>
}

package "Design Patterns" {
    component [FaaS Paradigm] <<F>>
    component [Event-Driven] <<E>>
    component [Memory Management] <<M>>
    component [Strategy Pattern] <<S>>
    component [Template Method Pattern] <<T>>
    component [Platform Dependent] <<P>>
}

[FastCGI Integration] -right-> [Function Mapping]
[Function Mapping] -right-> [Request Handling]
[Request Handling] -right-> [Multi-threading]

[ffunc.h] -right-> [ffunc.c]
[ffunc.c] -right-> [CMakeLists.txt]
[profile_service.c/cpp] -right-> [ffunc.h]
[DockerExample/*] -right-> [ffunc.c]
[README.md] -right-> [DockerExample/*]

[Memory Management] -right-> [Strategy Pattern]
[Strategy Pattern] -right-> [Template Method Pattern]
[Template Method Pattern] -right-> [Platform Dependent]

note left of [Configuration]
  Defines server parameters such as socket port, backlog, 
  max threads, and function mappings.
end note

note right of [README.md]
  Contains building, configuration, and usage instructions.
end note

@enduml
"""

# Create a PlantUML object and compile the diagram
plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
try:
    plantuml.processes(diagram)
except Exception as e:
    print(f"An error occurred: {e}")