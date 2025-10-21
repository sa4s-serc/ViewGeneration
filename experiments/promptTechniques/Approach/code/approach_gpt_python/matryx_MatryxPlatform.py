from plantuml import PlantUML

plantuml_code = """
@startuml
title Matryx Platform Architecture

package "Smart Contracts (Solidity)" {
    class MatryxPlatform {
        +manageTournaments()
        +manageSubmissions()
        +manageCommits()
        +forwardCalls()
    }
    class MatryxSystem {
        +manageVersions()
        +manageLibraryAddresses()
    }
    class MatryxForwarder {
        +forwardCalls()
    }
    class LibPlatform {
        +coreLogic()
    }
    class LibCommit {
        +coreLogic()
    }
    class LibTournament {
        +coreLogic()
    }
    class MatryxToken {
        +ERC20Implementation()
    }
}

package "Javascript/Build" {
    class truffle_config {
        +networkSettings()
        +compilerOptions()
    }
    class test {
        +integrationTests()
    }
    class benchmark {
        +measureGasUsage()
    }
    class utils {
        +utilityFunctions()
    }
    class network {
        +ethereumNetworkConfig()
    }
}

package "Documentation" {
    class index {
        +overview()
    }
    class searchtools {
        +searchFunctions()
    }
}

MatryxPlatform --> MatryxSystem : uses
MatryxPlatform --> MatryxForwarder : uses
MatryxPlatform --> LibPlatform : delegatecall
MatryxPlatform --> LibCommit : delegatecall
MatryxPlatform --> LibTournament : delegatecall
MatryxPlatform --> MatryxToken : uses

truffle_config --> test : setup
truffle_config --> benchmark : setup
truffle_config --> utils : setup
truffle_config --> network : setup

index --> searchtools : references

@enduml
"""

url = "http://www.plantuml.com/plantuml/img/"
uml = PlantUML(url)
uml.processes(plantuml_code)