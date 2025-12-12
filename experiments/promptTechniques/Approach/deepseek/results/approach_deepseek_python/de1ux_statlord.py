from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import React, Django
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.ci import Jenkins
from diagrams.aws.network import CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2

with Diagram("Statlord Dashboard Application Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend"):
        react_app = React("Dashboard Editor")
        viewer = React("Dashboard Viewer")
        frontend_components = [react_app, viewer]
    
    with Cluster("Backend"):
        django_api = Django("Django REST API")
        
        with Cluster("Database"):
            postgres = PostgreSQL("PostgreSQL")
            redis_cache = Redis("Redis Cache")
        
        django_api >> postgres
        django_api >> redis_cache
    
    with Cluster("External Data Sources"):
        api_source = Server("External API")
        mock_data = Server("Mock Data Generator")
    
    with Cluster("Display Devices"):
        browser = User("Browser Display")
        raspberry_pi = Server("Raspberry Pi")
        arduino = Server("Arduino")
        display_devices = [browser, raspberry_pi, arduino]
    
    with Cluster("Infrastructure"):
        with Cluster("Containerization"):
            docker_container = Docker("Docker Container")
        
        with Cluster("Web Server"):
            nginx_server = Nginx("Nginx")
        
        with Cluster("CI/CD"):
            jenkins_pipeline = Jenkins("Jenkins")
        
        with Cluster("Cloud Services"):
            cloudfront = CloudFront("CloudFront CDN")
            s3_bucket = S3("S3 Storage")
            ec2_instance = EC2("EC2 Instance")
    
    # Connections
    user >> react_app
    user >> viewer
    
    react_app >> django_api
    viewer >> django_api
    
    django_api >> api_source
    django_api >> mock_data
    
    django_api >> browser
    django_api >> raspberry_pi
    django_api >> arduino
    
    django_api >> docker_container
    docker_container >> nginx_server
    nginx_server >> cloudfront
    cloudfront >> s3_bucket
    jenkins_pipeline >> ec2_instance