from plantuml import PlantUML

plantuml_code = """
@startuml
skinparam componentStyle rectangle

package "ballerina-platform_asyncapi-tools" {
  [AsyncAPI/OpenAPI Code Generation] <<service>> #LightBlue
  [Ballerina to AsyncAPI Export] <<service>> #LightGreen
  [WebSocket Support] <<module>> #LightYellow
  [Authentication Handling] <<module>> #LightCoral
  [AsyncAPI CLI Tooling] <<interface>> #LightGrey
  [Data Structure Handling] <<module>> #LightSalmon
  [Error Handling] <<module>> #LightPink

  [zoom.yaml] <<artifact>> #LightCyan
  [ably.yaml] <<artifact>> #LightCyan
  [stripe.yaml] <<artifact>> #LightCyan
  [/schema/] <<artifact>> #LightCyan
  [/schema/baloutputs/] <<artifact>> #LightCyan
  [/websockets/ballerina-to-asyncapi/] <<artifact>> #LightCyan

  [AsyncApiCmd.java] <<artifact>> #LightSteelBlue
  [AsyncApiToBallerinaGenerator.java] <<artifact>> #LightSteelBlue
  [BallerinaToAsyncApiGenerator.java] <<artifact>> #LightSteelBlue
  [Ballerina.toml] <<artifact>> #LightSteelBlue
  [Dependencies.toml] <<artifact>> #LightSteelBlue
  [*Tests.java] <<artifact>> #LightSteelBlue

  [AsyncAPI/OpenAPI Code Generation] -right-> [Ballerina to AsyncAPI Export]
  [AsyncAPI/OpenAPI Code Generation] -down-> [WebSocket Support]
  [Ballerina to AsyncAPI Export] -down-> [Authentication Handling]
  [AsyncAPI CLI Tooling] -left-> [Data Structure Handling]
  [Error Handling] -left-> [AsyncAPI CLI Tooling]

  [zoom.yaml] -right-> [AsyncAPI/OpenAPI Code Generation]
  [ably.yaml] -right-> [AsyncAPI/OpenAPI Code Generation]
  [stripe.yaml] -right-> [AsyncAPI/OpenAPI Code Generation]
  [/schema/] -left-> [AsyncAPI/OpenAPI Code Generation]
  [/schema/baloutputs/] -left-> [Ballerina to AsyncAPI Export]
  [/websockets/ballerina-to-asyncapi/] -left-> [WebSocket Support]

  [AsyncApiCmd.java] -down-> [AsyncAPI CLI Tooling]
  [AsyncApiToBallerinaGenerator.java] -down-> [AsyncAPI/OpenAPI Code Generation]
  [BallerinaToAsyncApiGenerator.java] -down-> [Ballerina to AsyncAPI Export]
  [Ballerina.toml] -down-> [AsyncAPI CLI Tooling]
  [Dependencies.toml] -down-> [AsyncAPI CLI Tooling]
  [*Tests.java] -down-> [Error Handling]
}

@enduml
"""

# Create a PlantUML object and generate the diagram
uml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
uml.processes(plantuml_code)