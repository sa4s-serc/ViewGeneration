from plantuml import PlantUML

def generate_architecture_diagram():
    diagram = """
@startuml
skinparam componentStyle uml2
skinparam linetype ortho

title Scrumlr.io Architecture

' Define components
package "Frontend (TypeScript/React)" {
    [React Application] as frontend
    [Redux Store] as store
    [Components] as components
}

package "Backend (Go)" {
    [API Server] as api
    [Board Service] as boardService
    [Note Service] as noteService
    [User Service] as userService
    [Auth Service] as authService
    [Database Layer] as dbLayer
    [WebSocket Handler] as wsHandler
}

package "Storage & Messaging" {
    database "PostgreSQL" as db
    queue "NATS" as nats
    database "Redis" as redis
}

package "Authentication" {
    [OAuth Providers] as oauth
}

' Define relationships
frontend --> api : HTTP/REST
frontend --> wsHandler : WebSocket
components --> store : state updates
store --> frontend : data flow

api --> boardService
api --> noteService 
api --> userService
api --> authService

wsHandler --> nats : pub/sub
wsHandler --> redis : session/cache

boardService --> dbLayer
noteService --> dbLayer
userService --> dbLayer
dbLayer --> db : SQL

authService --> oauth : delegates auth

@enduml
"""

    # Save diagram to file
    with open('architecture.puml', 'w') as f:
        f.write(diagram)

    # Generate diagram
    server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    server.processes_file('architecture.puml', outfile='scrumlr_architecture.png')

if __name__ == "__main__":
    generate_architecture_diagram()