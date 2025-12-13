import diagrams
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.generic.os import LinuxGeneral

with Diagram("IBM Spectrum Scale Security Posture Monitoring System", show=False, direction="TB"):
    internet = Internet("Internet")
    
    with Cluster("Spectrum Scale Cluster"):
        scale_cluster = Server("GPFS Cluster")
        collector = Python("security_posture.py")
        scale_cluster >> collector
    
    with Cluster("Monitoring System"):
        with Cluster("Data Collection"):
            cron = Python("cronjob.py")
            fetch_script = Python("fetch_security_posture_and_upload_to_ES.sh")
            split_script = Python("split_json_for_kibana.py")
            
            cron >> fetch_script
            fetch_script >> split_script
        
        with Cluster("Configuration"):
            scale_conf = Storage("scale-clusters.conf")
            security_conf = Storage("security-posture.conf")
        
        with Cluster("Data Processing"):
            json_data = Storage("JSON Data")
            split_script >> json_data
        
        with Cluster("Elasticsearch Cluster"):
            es = ElasticsearchService("Elasticsearch")
            kibana = Cloudwatch("Kibana Dashboard")
            json_data >> es
            es >> kibana
    
    # Connections
    collector >> fetch_script
    scale_conf >> fetch_script
    security_conf >> fetch_script
    internet >> scale_cluster
    internet >> kibana