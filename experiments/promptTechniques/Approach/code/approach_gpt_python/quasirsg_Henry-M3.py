from plantuml import PlantUML

def generate_architecture_diagram():
    plantuml_code = """
    @startuml
    skinparam componentStyle rectangle

    title Node.js/Express.js Learning Repository Architecture

    package "Asynchronous Programming & Promises" {
        [pledge.js] << (M, #FFAAAA) >> 
        [custom.matchers.js] << (M, #FFAAAA) >>
    }

    package "Node.js Fundamentals" {
        [server creation] << (M, #FFAAAA) >>
        [request handling] << (M, #FFAAAA) >>
        [event loops] << (M, #FFAAAA) >>
        [modules] << (M, #FFAAAA) >>
        [NPM management] << (M, #FFAAAA) >>
        [streams and buffers] << (M, #FFAAAA) >>
    }

    package "Express.js Web Application Development" {
        [index.js] << (C, #AAFFAA) >>
        [myapp/] << (C, #AAFFAA) >>
        [server.js] << (C, #AAFFAA) >>
        [routing] << (C, #AAFFAA) >>
        [middleware] << (C, #AAFFAA) >>
        [body-parser] << (C, #AAFFAA) >>
    }

    package "Software Testing" {
        [index.spec.js] << (T, #AAAAFF) >>
        [server.test.js] << (T, #AAAAFF) >>
        [pledge.spec.ch*.html] << (T, #AAAAFF) >>
    }

    [pledge.js] -- [custom.matchers.js] : uses
    [server creation] o-- [request handling] : supports
    [request handling] o-- [event loops] : involves
    [modules] o-- [NPM management] : aids
    [streams and buffers] o-- [server creation] : enhances

    [index.js] --> [routing] : maps
    [myapp/] --> [middleware] : processes
    [server.js] --> [body-parser] : parses

    [index.spec.js] --> [index.js] : tests
    [server.test.js] --> [server.js] : tests

    note right of [Express.js Web Application Development]
    Layered Architecture:
    - Routes
    - Views
    - Public
    end note

    note right of [Software Testing]
    TDD Principles:
    - Unit Testing
    - Integration Testing
    - End-to-End Testing
    end note

    @enduml
    """

    server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    response = server.processes(plantuml_code.encode('utf-8'))
    with open('architecture_diagram.png', 'wb') as f:
        f.write(response)

generate_architecture_diagram()