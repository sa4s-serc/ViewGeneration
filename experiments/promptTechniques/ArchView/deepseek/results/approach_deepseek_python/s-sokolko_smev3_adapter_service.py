from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.database import Mongodb
from diagrams.onprem.queue import Celery
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.workflow import Airflow
from diagrams.programming.framework import FastAPI
from diagrams.programming.language import Python

with Diagram("SMEV3 Adapter Service Architecture", show=False, direction="LR"):
    users = User("External Clients")
    
    api_gateway = Nginx("API Gateway")
    
    sanic_app = FastAPI("Sanic Application")
    
    views = Python("Views Layer")
    query_processor = Python("Query Processor")
    adapter = Python("SMEV3 Adapter")
    schema_loader = Python("Schema Loader")
    
    mongodb = Mongodb("MongoDB")
    redis_cache = Redis("Redis Cache")
    celery_worker = Celery("Celery Worker")
    airflow = Airflow("Airflow Scheduler")
    
    smev3_adapter = Docker("SMEV3 Adapter Service")
    
    users >> api_gateway >> sanic_app
    
    sanic_app >> views
    views >> query_processor
    query_processor >> adapter
    adapter >> smev3_adapter
    
    query_processor >> schema_loader
    schema_loader >> mongodb
    
    query_processor >> mongodb
    query_processor >> redis_cache
    
    celery_worker >> query_processor
    airflow >> celery_worker