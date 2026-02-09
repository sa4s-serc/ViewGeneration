from diagrams import Diagram, Cluster
from diagrams.onprem.network import Apache
from diagrams.onprem.database import MySQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import Spring
from diagrams.programming.language import PHP

with Diagram("CodeIgniter Application Architecture", show=False, direction="TB"):
    front_controller = Apache("Front Controller\nindex.php")
    
    with Cluster("MVC Layer"):
        controller = PHP("Controller")
        facade = Spring("Facade")
        business_logic = Spring("Business Logic")
    
    with Cluster("Data Access Layer"):
        factory_business = Spring("FactoryBusiness")
        factory_dao = Spring("FactoryDAO")
        generic_dao = Spring("GenericDAO")
        dao = Spring("DAO")
    
    with Cluster("Persistence"):
        database = MySQL("Database")
        cache = Redis("Cache")
        message_queue = Kafka("Message Queue")
    
    front_controller >> controller
    controller >> facade
    facade >> business_logic
    business_logic >> factory_business
    factory_business >> factory_dao
    factory_dao >> generic_dao
    generic_dao >> dao
    dao >> database
    dao >> cache
    business_logic >> message_queue