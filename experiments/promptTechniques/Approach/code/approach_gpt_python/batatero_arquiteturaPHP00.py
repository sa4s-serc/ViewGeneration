from plantuml import PlantUML

plantuml_code = """
@startuml
skinparam componentStyle rectangle
skinparam backgroundColor #F3F3F3
skinparam ArrowColor #66B2FF
skinparam RectangleColor #LightBlue

package "CodeIgniter Application" {
    component "Controller" as Controller
    component "Facade" as Facade
    component "Business Logic" as BusinessLogic
    component "DAO" as DAO
    component "GenericDAO" as GenericDAO
    component "FactoryBusiness" as FactoryBusiness
    component "FactoryDAO" as FactoryDAO
}

Controller --> Facade : uses
Facade --> BusinessLogic : calls
BusinessLogic --> DAO : interacts
FactoryBusiness -> BusinessLogic : creates
FactoryDAO -> DAO : creates

GenericDAO <|-- DAO : extends

@enduml
"""

server = PlantUML(url='http://www.plantuml.com/plantuml/png/')
server.processes(plantuml_code)