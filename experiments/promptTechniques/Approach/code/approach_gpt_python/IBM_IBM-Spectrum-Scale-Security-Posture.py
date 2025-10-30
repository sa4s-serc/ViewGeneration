from diagrams import Diagram
from diagrams.custom import Custom
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.analytics import ElasticsearchService
from diagrams.onprem.client import Client
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

with Diagram("IBM Spectrum Scale Security Posture Monitoring System", show=False):
    client = Client("User")
    nginx = Nginx("Web Server")
    client >> nginx

    with Diagram("Spectrum Scale Cluster", direction="TB"):
        collector = Custom("collector/security_posture.py", "./icons/python.png")
        json_splitter = Custom("split_json_for_kibana.py", "./icons/python.png")
        cronjob = Custom("cronjob.py", "./icons/python.png")
        es_uploader = Custom("fetch_security_posture_and_upload_to_ES.sh", "./icons/bash.png")

        collector >> json_splitter >> es_uploader >> ElasticsearchService("Elasticsearch")
        cronjob >> collector

    with Diagram("Configuration Files", direction="TB"):
        conf1 = Custom("security-posture.conf", "./icons/conf.png")
        conf2 = Custom("scale-clusters.conf", "./icons/conf.png")
    
    cronjob << conf1
    collector << conf2

    with Diagram("External Tools", direction="TB"):
        ssh = Custom("SSH", "./icons/ssh.png")
        scp = Custom("SCP", "./icons/scp.png")
        curl = Custom("CURL", "./icons/curl.png")
        mm_commands = Custom("mm commands", "./icons/commands.png")

    collector >> ssh
    es_uploader >> scp
    es_uploader >> curl
    collector >> mm_commands