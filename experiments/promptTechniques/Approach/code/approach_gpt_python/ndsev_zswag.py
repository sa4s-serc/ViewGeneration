from plantuml import PlantUML

diagram = """
@startuml
!define RECTANGLE(x) rectangle x
!define COMPONENT(x) component x

skinparam componentStyle rectangle
skinparam legendBackgroundColor #f3f3f3
skinparam legendBorderColor #000000

package "zswag Project Analysis" {
  RECTANGLE("OpenAPI Generation (zswag.gen)") {
    COMPONENT("zswag.gen CLI Tool")
  }

  RECTANGLE("Python Server (OAServer)") {
    COMPONENT("Flask/Connexion Server")
    COMPONENT("Controller Modules")
  }

  RECTANGLE("Python Client (OAClient)") {
    COMPONENT("Generic Python Client")
  }

  RECTANGLE("C++ Client (OAClient)") {
    COMPONENT("zswagcl Library")
    COMPONENT("pyzswagcl Python Bindings")
  }

  RECTANGLE("HTTP Client Library (httpcl)") {
    COMPONENT("cpp-httplib Wrapper")
  }
}

"zswag.gen CLI Tool" --> "Flask/Connexion Server" : Generates OpenAPI
"Flask/Connexion Server" --> "Generic Python Client" : Hosts as OpenAPI
"Generic Python Client" --> "zswagcl Library" : Interacts via REST
"zswagcl Library" --> "cpp-httplib Wrapper" : Uses for HTTP

legend
  |= Component |= Description |
  | zswag.gen CLI Tool | Generates OpenAPI YAML from Zserio |
  | Flask/Connexion Server | Hosts Zserio services as OpenAPI |
  | Generic Python Client | Interacts with Zserio services via REST |
  | zswagcl Library | C++ library for OpenAPI client |
  | cpp-httplib Wrapper | Provides HTTP communication |
endlegend

@enduml
"""

server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
server.processes(diagram)