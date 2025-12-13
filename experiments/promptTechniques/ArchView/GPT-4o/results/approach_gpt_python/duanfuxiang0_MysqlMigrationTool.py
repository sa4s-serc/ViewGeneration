from plantuml import PlantUML

plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')

diagram = """
@startuml

package "Incremental Data Migration Tool" {
    component "MySQL Database" as mysql_db
    component "Binlog Capture and Parsing" as binlog_parsing
    component "Data Type Handling" as data_type_handling
    component "Data Mapping" as data_mapping
    component "Database Operations" as db_operations
    component "Error Handling" as error_handling

    mysql_db --> binlog_parsing : "Binlog Events"
    binlog_parsing --> data_type_handling : "Parsed Events"
    data_type_handling --> data_mapping : "Typed Data"
    data_mapping --> db_operations : "Mapped Data"
    db_operations --> mysql_db : "SQL Queries"
    binlog_parsing --> error_handling : "Process Events"
}

package "Key Files" {
    file "incremental_data_migration.go" as incremental
    file "full_data_migration.go" as full_migration
    file "core/dao.go" as dao
    file "core/conf.go" as conf

    incremental --> binlog_parsing
    incremental --> error_handling
    full_migration --> db_operations
    dao --> data_mapping
    dao --> db_operations
    conf --> error_handling
}

note right of mysql_db
    MySQL database as the
    source and destination
end note

@enduml
"""

with open('architecture_diagram.txt', 'w') as f:
    f.write(diagram)

print(plantuml.processes_file('architecture_diagram.txt'))