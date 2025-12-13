from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.elastic.elasticsearch import Elasticsearch 
from diagrams.elastic.elasticsearch import Kibana
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Users
from diagrams.onprem.network import Ssh
from diagrams.programming.flowchart import Document

with Diagram("IBM Spectrum Scale Security Posture Monitoring", show=False):

    with Cluster("Monitoring Infrastructure"):
        es = Elasticsearch("Elasticsearch")
        kb = Kibana("Kibana Dashboard")
        
    with Cluster("Data Collection"):
        collector = Python("security_posture.py")
        splitter = Python("split_json_for_kibana.py")
        uploader = Document("upload_to_ES.sh") 
        scheduler = Python("cronjob.py")
        
    with Cluster("Scale Clusters"):
        clusters = Server("Spectrum Scale\nClusters")
        
    users = Users("Administrators")

    # Define data flow
    users >> kb
    kb >> es
    scheduler >> collector
    clusters >> collector
    collector >> splitter
    splitter >> uploader
    uploader >> es