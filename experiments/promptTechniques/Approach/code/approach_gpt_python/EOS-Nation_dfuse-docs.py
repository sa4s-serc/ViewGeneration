from plantuml import PlantUML

uml_code = """
@startuml
skinparam componentStyle rectangle
skinparam nodesep 30

package "dfuse-based System" {

  rectangle "mindreader" as MR
  rectangle "relayer" as RL
  rectangle "search" as SC
  rectangle "dgraphql" as DG
  
  rectangle "GraphQL API" as GQL
  rectangle "Data Indexing" as DI
  rectangle "Streaming Data" as SD
  rectangle "dfuseeos CLI" as CLI
  rectangle "Authentication & Authorization" as AA
  rectangle "nodeos Integration" as NI
  rectangle "Data Storage" as DS
  rectangle "Multi-Chain Support" as MCS

  database "BigTable" as BT
  database "TiKV" as TIKV
  database "Badger" as BD
  
  MR --> DI : data extraction
  DI --> SC : data indexing
  SC --> GQL : API serving
  SC --> SD : data streaming
  CLI --> GQL : API access
  GQL --> AA : provides
  GQL --> MCS : supports
  GQL --> NI : integrates
  MCS --> NI : interacts with
  DI --> DS : stores data
  DS --> BT : uses
  DS --> TIKV : uses
  DS --> BD : uses

  note right of MR
    Microservice Architecture:
    - mindreader
    - relayer
    - search
    - dgraphql
  end note

  note right of GQL
    GraphQL API:
    - flexible
    - efficient
    - real-time
  end note

  note right of DI
    Data Indexing & Search:
    - defined query language
  end note

  note right of SD
    Streaming Data:
    - real-time
    - handles forks
  end note

  note right of DS
    Hierarchical Storage:
    - object stores
    - databases
  end note

}

@enduml
"""

server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
server.processes(uml_code)