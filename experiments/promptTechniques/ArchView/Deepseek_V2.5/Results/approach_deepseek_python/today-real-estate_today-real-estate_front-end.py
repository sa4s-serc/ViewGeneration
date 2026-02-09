from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import Vue
from diagrams.programming.language import Javascript
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.aws.network import CloudFront
from diagrams.aws.mobile import APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.gcp.analytics import BigQuery
from diagrams.azure.compute import ContainerInstances
from diagrams.azure.database import CosmosDb
from diagrams.azure.network import CDNProfiles

with Diagram("Real Estate Frontend Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Frontend Layer"):
        frontend = Vue("Vue.js App")
        vuex = Javascript("Vuex Store")
        router = Javascript("Vue Router")
        components = Javascript("Components")
        
        frontend - vuex
        frontend - router
        frontend - components
    
    with Cluster("API Layer"):
        api_gateway = APIGateway("API Gateway")
        auth_api = Lambda("Auth API")
        user_api = Lambda("User API")
        search_api = Lambda("Search API")
        news_api = Lambda("News API")
        inquiry_api = Lambda("Inquiry API")
        
        api_gateway >> auth_api
        api_gateway >> user_api
        api_gateway >> search_api
        api_gateway >> news_api
        api_gateway >> inquiry_api
    
    with Cluster("Backend Services"):
        recommendation_service = ContainerInstances("Recommendation Service")
        map_service = ContainerInstances("Kakao Map Service")
        notification_service = Lambda("Notification Service")
    
    with Cluster("Data Layer"):
        postgres_db = RDS("PostgreSQL")
        redis_cache = Redis("Redis Cache")
        s3_storage = S3("File Storage")
        cosmos_db = CosmosDb("NoSQL Data")
        bigquery = BigQuery("Analytics")
    
    with Cluster("External Services"):
        kakao_maps = Nginx("Kakao Maps API")
        external_news = Nginx("News API")
        email_service = Nginx("Email Service")
    
    cdn = CloudFront("CDN")
    azure_cdn = CDNProfiles("Azure CDN")
    
    user >> frontend
    frontend >> cdn
    frontend >> api_gateway
    
    auth_api >> postgres_db
    user_api >> postgres_db
    search_api >> postgres_db
    search_api >> redis_cache
    news_api >> external_news
    inquiry_api >> postgres_db
    inquiry_api >> email_service
    
    api_gateway >> recommendation_service
    api_gateway >> map_service
    api_gateway >> notification_service
    
    recommendation_service >> postgres_db
    recommendation_service >> redis_cache
    map_service >> kakao_maps
    notification_service >> email_service
    
    postgres_db >> bigquery
    redis_cache >> bigquery
    
    s3_storage >> cdn
    components >> azure_cdn