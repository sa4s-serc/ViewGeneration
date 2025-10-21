from plantuml import PlantUML

# Define the server
server = PlantUML(url='http://www.plantuml.com/plantuml/uml/')

# UML diagram source for a Clean Architecture with Ports and Adapters pattern
uml_code = """
@startuml
!define ENTITY #FFCC00
!define USECASE #FF9999
!define PROVIDER #99FF99
!define CONTROLLER #9999FF
!define GRPC #FF99FF

package "entities" <<ENTITY>> {
    class LedgerEntry
    class FinancialInstitution
    class AccountHolder
    class Account
    class Consent
    class PaymentInstruction
    class PaymentTransaction
}

package "usecases" <<USECASE>> {
    class ModelBankUsecase {
        +processPayment()
        +manageAccount()
    }
    ModelBankUsecase -> "ModelBankEntityGateway" : depends
}

package "providers" <<PROVIDER>> {
    class DbProvider {
        +createSchema()
        +CRUD()
    }
    class ModelBankController {
        +handleRequest()
    }
    DbProvider -> "ModelBankEntityGateway" : implements
}

package "controllers" <<CONTROLLER>> {
    class ModelBankController {
        +invokeUsecase()
        +presentResults()
    }
    ModelBankController -> "ModelBankUsecaseInputPort" : uses
}

package "grpc" <<GRPC>> {
    class ModelBankService {
        +CreateConsent()
    }
}

ModelBankService -> ModelBankController : calls
ModelBankUsecase -> LedgerEntry : uses
ModelBankUsecase -> FinancialInstitution : uses
ModelBankUsecase -> AccountHolder : uses
ModelBankUsecase -> Account : uses
ModelBankUsecase -> Consent : uses
ModelBankUsecase -> PaymentInstruction : uses
ModelBankUsecase -> PaymentTransaction : uses

ModelBankEntityGateway <|-- DbProvider
ModelBankUsecaseInputPort <|-- ModelBankController
ModelBankControllerOutputPort <|-- ModelBankController
ModelBankUsecaseOutputPort <|-- ModelBankUsecase

@enduml
"""

# Send the UML code to the server and get the URL
response = server.processes(uml_code)
print(response)  # Corrected to print the response directly without indexing as a dictionary