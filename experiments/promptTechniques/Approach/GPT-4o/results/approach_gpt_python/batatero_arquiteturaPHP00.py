from diagrams import Diagram, Cluster, Edge
from diagrams.programming.flowchart import PredefinedProcess, ManualInput
from diagrams.onprem.database import PostgreSQL, MariaDB
from diagrams.onprem.network import Apache, Nginx
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.ci import Jenkins

with Diagram("CodeIgniter and Doctrine ORM Architecture", show=False, direction="LR"):

    with Cluster("CodeIgniter Application"):
        controller = PredefinedProcess("Controller")
        facade = PredefinedProcess("Facade")
        business_logic = PredefinedProcess("Business Logic")
        dao = PredefinedProcess("DAO")
        factory_business = PredefinedProcess("FactoryBusiness")
        factory_dao = PredefinedProcess("FactoryDAO")

        controller >> facade >> business_logic >> dao
        factory_business >> business_logic
        factory_dao >> dao

    with Cluster("Core Files"):
        index_php = ManualInput("index.php")
        config_files = [ManualInput("config.php"), ManualInput("autoload.php"), ManualInput("database.php")]

    with Cluster("CodeIgniter Libraries"):
        core_libraries = [
            Apache("Input"),
            Nginx("Security"),
            Redis("Email"),
            RabbitMQ("Session"),
            Docker("Image_lib"),
            Airflow("XMLRPC"),
            Jenkins("Javascript"),
            Grafana("Table"),
            Prometheus("Upload"),
        ]

    controller >> core_libraries

    with Cluster("Doctrine ORM"):
        platform_abstraction = PredefinedProcess("Platform Abstraction")
        schema_management = PredefinedProcess("Schema Management")
        annotation_parsing = PredefinedProcess("Annotation Parsing")
        object_management = PredefinedProcess("Object Management")
        querying = PredefinedProcess("Querying")
        hydration = PredefinedProcess("Hydration")
        unit_of_work = PredefinedProcess("Unit of Work")
        caching = PredefinedProcess("Caching")

        platform_abstraction >> schema_management >> annotation_parsing >> object_management >> querying >> hydration >> unit_of_work >> caching

    with Cluster("Databases"):
        db_postgresql = PostgreSQL("PostgreSQL")
        db_mariadb = MariaDB("MariaDB")

    doctrine_components = [
        platform_abstraction,
        schema_management,
        annotation_parsing,
        object_management,
        querying,
        hydration,
        unit_of_work,
        caching,
    ]

    doctrine_components >> Edge(color="brown") >> db_postgresql
    doctrine_components >> Edge(color="brown") >> db_mariadb
    controller >> Edge(color="blue") >> db_postgresql
    controller >> Edge(color="blue") >> db_mariadb