import tiktoken

# Replace this with your actual input string
input_string ="""@startuml
skinparam rectangle {
  BackgroundColor white
  BorderColor black
  Style roundrect
}
skinparam defaultTextAlignment center
skinparam componentStyle rectangle

rectangle "<b>Client-side" as client_side {
  frame "Technology" {
    rectangle "Angular 7" as Angular
  }

  frame "Logic" {
    rectangle "UI Components" as UI {
      rectangle "HTML\\nTemplates" as HTML
      rectangle "Component\\nClass" as Component
    }
    rectangle "Angular Services" as AngularServices
    HTML --> AngularServices
    Component --> AngularServices
  }

  frame "Data" {
    rectangle "ngRX state store" as ngrx
    rectangle "View-Models\\n(JSON)" as ViewModelJson
  }

  AngularServices -down-> Angular : HTTP
}

rectangle "<b>Server-side" as server_side {
  frame "WebAPI (.NET Core)" {
    rectangle ".NET Core\\nWebAPI" as WebAPI
    rectangle "Standard\\nC# Classes" as CSharp
    rectangle "Entity Framework\\n(ORM)" as EF
    WebAPI --> CSharp
    CSharp --> EF
  }

  frame "Controller Layer" {
    rectangle "WebAPI\\nControllers" as Controllers
    rectangle "Domain Services" as Domain {
      rectangle "PDF" as PDF
      rectangle "CAPTCHA" as CAPTCHA
      rectangle "Email" as Email
    }
    Controllers --> PDF
    Controllers --> CAPTCHA
    Controllers --> Email

    rectangle "DbContext" as DbContext
    Email --> DbContext
  }

  frame "Data Layer" {
    rectangle "View-Models\\n(C#)" as ViewModelCSharp
    rectangle "DB Entities\\n(Registration, Community, etc.)" as DBEntities
  }
}

AngularServices -right-> WebAPI : HTTP
AngularServices -right-> Controllers : HTTP
ViewModelJson -right-> ViewModelCSharp
EF --> DBEntities
DbContext --> DBEntities

@enduml"""
# Choose an encoding — usually 'cl100k_base' for GPT-4, GPT-3.5-turbo, etc.
encoding = tiktoken.get_encoding("cl100k_base")

# Tokenize the string
tokens = encoding.encode(input_string)

# Print tokens and their decoded form
print("Total tokens:", len(tokens))
