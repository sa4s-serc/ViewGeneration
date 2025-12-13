from diagrams import Diagram
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.database import Mongodb
from diagrams.custom import Custom

with Diagram("Microservices Architecture", show=False):
    catalog_service = Custom("Catalog Microservice", "./icons/dotnet.png")
    customer_service = Custom("Customer Microservice", "./icons/dotnet.png")
    order_service = Custom("Order Microservice", "./icons/dotnet.png")

    rabbitmq = Rabbitmq("RabbitMQ")

    catalog_db = Mongodb("Catalog DB")
    customer_db = Mongodb("Customer DB")
    order_db = Mongodb("Order DB")

    catalog_service >> rabbitmq
    customer_service >> rabbitmq
    order_service >> rabbitmq

    rabbitmq >> catalog_service
    rabbitmq >> customer_service
    rabbitmq >> order_service

    catalog_service >> catalog_db
    customer_service >> customer_db
    order_service >> order_db