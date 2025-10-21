from plantuml import PlantUML

# Define PlantUML server
server = PlantUML(url='http://www.plantuml.com/plantuml/uml/')

# UML diagram representation
uml_code = """
@startuml
!define RECTANGLE
!define ELLIPSE

package "scrumlr.io Architecture" {
  RECTANGLE "Backend (Go)" {
    RECTANGLE "Server" as Server
    RECTANGLE "Database Layer" as DatabaseLayer
    RECTANGLE "Realtime Communication" as RealtimeCommunication
    RECTANGLE "Authentication" as Authentication
    RECTANGLE "API Handlers" as APIHandlers
    RECTANGLE "Business Logic" as BusinessLogic
  }

  RECTANGLE "Frontend (TypeScript/React)" {
    RECTANGLE "React Components" as ReactComponents
    RECTANGLE "Redux Store" as ReduxStore
    RECTANGLE "Routes" as Routes
  }

  RECTANGLE "Infrastructure" {
    RECTANGLE "Docker Setup" as DockerSetup
    RECTANGLE "CI/CD Workflows" as CICDWorkflows
  }

  ELLIPSE "External Services" {
    ELLIPSE "Google Auth" as GoogleAuth
    ELLIPSE "GitHub Auth" as GitHubAuth
    ELLIPSE "Microsoft Auth" as MicrosoftAuth
    ELLIPSE "NATS Messaging" as NATSMessaging
    ELLIPSE "Redis" as Redis
  }
  
  Server --> DatabaseLayer : "Bun ORM"
  Server <--> RealtimeCommunication : "WebSockets"
  Server --> Authentication : "Auth Logic"
  Server --> APIHandlers : "HTTP Endpoints"
  APIHandlers --> BusinessLogic : "Service Calls"
  ReactComponents --> ReduxStore : "State Management"
  ReactComponents <--> Routes : "Routing"
  DockerSetup --> Server : "Containerization"
  DockerSetup --> ReactComponents : "Containerization"
  DockerSetup --> DatabaseLayer : "Containerization"
  DockerSetup --> NATSMessaging : "Containerization"
  DockerSetup --> Redis : "Containerization"
  DockerSetup --> CICDWorkflows : "CI/CD"
  
  Authentication --> GoogleAuth : "OAuth"
  Authentication --> GitHubAuth : "OAuth"
  Authentication --> MicrosoftAuth : "OAuth"
  RealtimeCommunication --> NATSMessaging : "Event Bus"
  RealtimeCommunication --> Redis : "Sync"
}

@enduml
"""

# Generate and save the diagram
server.processes(uml_code, infile='scrumlr_architecture.uml', outfile='scrumlr_architecture.png')