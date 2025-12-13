from diagrams import Diagram, Cluster
from diagrams.aws.network import VPC, InternetGateway, RouteTable, PublicSubnet, PrivateSubnet, ELB, CloudFront
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM
from diagrams.onprem.network import Nginx
from diagrams.aws.analytics import ElasticsearchService

with Diagram("OpenSearch Dashboard Nginx Proxy Architecture", show=False, direction="TB"):
    internet = InternetGateway("Internet")
    
    with Cluster("VPC"):
        with Cluster("Public Subnet"):
            nginx_proxy = Nginx("Nginx Proxy")
            elastic_ip = ELB("Elastic IP")
        
        with Cluster("Private Subnet"):
            opensearch_dashboard = ElasticsearchService("OpenSearch Dashboard")
        
        security_group = IAM("Security Groups")
        route_table = RouteTable("Route Table")
    
    internet >> elastic_ip >> nginx_proxy
    nginx_proxy >> opensearch_dashboard
    
    security_group - [nginx_proxy, opensearch_dashboard]
    route_table - [nginx_proxy, opensearch_dashboard]